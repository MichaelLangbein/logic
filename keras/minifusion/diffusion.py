#%%
import keras
import keras as k
import tensorflow as tf
import keras.layers as l


#%%



class PaddedConv2D(l.Layer):
    def __init__(self, filters, kernel_size, padding=0, strides=1, **kwargs):
        super().__init__(**kwargs)
        self.padding2d = l.ZeroPadding2D(padding)
        self.conv2d = l.Conv2D(filters, kernel_size, strides=strides)

    def call(self, inputs):
        x = self.padding2d(inputs)
        return self.conv2d(x)


class ResBlock(l.Layer):
    def __init__(self, output_dim, **kwargs):
        super().__init__(**kwargs)
        self.output_dim = output_dim
        self.entry_flow = [
            l.GroupNormalization(groups=output_dim//10, epsilon=1e-5),
            l.Activation("swish"),
            PaddedConv2D(output_dim, 3, padding=1),
        ]
        self.embedding_flow = [
            l.Activation("swish"),
            l.Dense(output_dim),
        ]
        self.exit_flow = [
            l.GroupNormalization(groups=output_dim//10, epsilon=1e-5),
            l.Activation("swish"),
            PaddedConv2D(output_dim, 3, padding=1),
        ]

    def build(self, input_shape):
        if input_shape[0][-1] != self.output_dim:
            self.residual_projection = PaddedConv2D(self.output_dim, 1)
        else:
            self.residual_projection = lambda x: x

    def call(self, inputs):
        inputs, embeddings = inputs
        x = inputs
        for layer in self.entry_flow:
            x = layer(x)
        for layer in self.embedding_flow:
            embeddings = layer(embeddings)
        x = x + embeddings[:, None, None]
        for layer in self.exit_flow:
            x = layer(x)
        return x + self.residual_projection(inputs)


class SpatialTransformer(l.Layer):
    def __init__(self, num_heads, head_size, fully_connected=False, **kwargs):
        super().__init__(**kwargs)
        self.norm = l.GroupNormalization(groups=num_heads*head_size//10, epsilon=1e-5)
        channels = num_heads * head_size
        if fully_connected:
            self.proj1 = l.Dense(num_heads * head_size)
        else:
            self.proj1 = PaddedConv2D(num_heads * head_size, 1)
        self.transformer_block = BasicTransformerBlock(
            channels, num_heads, head_size
        )
        if fully_connected:
            self.proj2 = l.Dense(channels)
        else:
            self.proj2 = PaddedConv2D(channels, 1)

    def call(self, inputs):
        inputs, context = inputs
        _, h, w, c = inputs.shape
        x = self.norm(inputs)
        x = self.proj1(x)
        x = tf.reshape(x, (-1, h * w, c))
        x = self.transformer_block([x, context])
        x = tf.reshape(x, (-1, h, w, c))
        return self.proj2(x) + inputs


class BasicTransformerBlock(l.Layer):
    def __init__(self, dim, num_heads, head_size, **kwargs):
        super().__init__(**kwargs)
        self.norm1 = l.LayerNormalization(epsilon=1e-5)
        self.attn1 = CrossAttention(num_heads, head_size)
        self.norm2 = l.LayerNormalization(epsilon=1e-5)
        self.attn2 = CrossAttention(num_heads, head_size)
        self.norm3 = l.LayerNormalization(epsilon=1e-5)
        self.geglu = GEGLU(dim * 4)
        self.dense = l.Dense(dim)

    def call(self, inputs):
        inputs, context = inputs
        x = self.attn1([self.norm1(inputs), None]) + inputs
        x = self.attn2([self.norm2(x), context]) + x
        return self.dense(self.geglu(self.norm3(x))) + x


class CrossAttention(l.Layer):
    def __init__(self, num_heads, head_size, **kwargs):
        super().__init__(**kwargs)
        self.to_q = l.Dense(num_heads * head_size, use_bias=False)
        self.to_k = l.Dense(num_heads * head_size, use_bias=False)
        self.to_v = l.Dense(num_heads * head_size, use_bias=False)
        self.scale = head_size**-0.5
        self.num_heads = num_heads
        self.head_size = head_size
        self.out_proj = l.Dense(num_heads * head_size)

    def call(self, inputs):
        inputs, context = inputs
        context = inputs if context is None else context
        q, k, v = self.to_q(inputs), self.to_k(context), self.to_v(context)
        q = tf.reshape(q, (-1, inputs.shape[1], self.num_heads, self.head_size))
        k = tf.reshape(
            k, (-1, context.shape[1], self.num_heads, self.head_size)
        )
        v = tf.reshape(
            v, (-1, context.shape[1], self.num_heads, self.head_size)
        )

        q = tf.transpose(q, (0, 2, 1, 3))  # (bs, num_heads, time, head_size)
        k = tf.transpose(k, (0, 2, 3, 1))  # (bs, num_heads, head_size, time)
        v = tf.transpose(v, (0, 2, 1, 3))  # (bs, num_heads, time, head_size)

        score = td_dot(q, k) * self.scale
        weights = keras.activations.softmax(
            score
        )  # (bs, num_heads, time, time)
        attn = td_dot(weights, v)
        attn = tf.transpose(
            attn, (0, 2, 1, 3)
        )  # (bs, time, num_heads, head_size)
        out = tf.reshape(
            attn, (-1, inputs.shape[1], self.num_heads * self.head_size)
        )
        return self.out_proj(out)


class Upsample(l.Layer):
    def __init__(self, channels, **kwargs):
        super().__init__(**kwargs)
        self.ups = l.UpSampling2D(2)
        self.conv = PaddedConv2D(channels, 3, padding=1)

    def call(self, inputs):
        return self.conv(self.ups(inputs))


class GEGLU(l.Layer):
    def __init__(self, output_dim, **kwargs):
        super().__init__(**kwargs)
        self.output_dim = output_dim
        self.dense = l.Dense(output_dim * 2)

    def call(self, inputs):
        x = self.dense(inputs)
        x, gate = x[..., : self.output_dim], x[..., self.output_dim :]
        tanh_res = k.activations.tanh(
            gate * 0.7978845608 * (1 + 0.044715 * (gate**2))
        )
        return x * 0.5 * gate * (1 + tanh_res)


def td_dot(a, b):
    aa = tf.reshape(a, (-1, a.shape[2], a.shape[3]))
    bb = tf.reshape(b, (-1, b.shape[2], b.shape[3]))
    cc = k.backend.batch_dot(aa, bb)
    return tf.reshape(cc, (-1, a.shape[1], cc.shape[1], cc.shape[2]))


#%%

"""
    Lingo
        - context: prompt converted to latent
        - t_embed: time-step, converted to latent
        - latent: image, converted to latent

    Simplifications:
        - where original had dublicate blocks, this uses only one.
        - halved all layer-sizes
        - assumes grayscale image

"""

class MiniDiffusionModel(k.Model):
    def __init__(self, img_height=128, img_width=128, nr_channels=1, max_text_length=100, name=None):
        
        context = keras.layers.Input((max_text_length, 768))
        t_embed_input = keras.layers.Input((320,))
        latent = keras.layers.Input((img_height // 8, img_width // 8, nr_channels))

        t_emb = keras.layers.Dense(320)(t_embed_input)
        t_emb = keras.layers.Activation("swish")(t_emb)
        t_emb = keras.layers.Dense(320)(t_emb)

        # Downsampling flow

        outputs = []
        x = PaddedConv2D(80, kernel_size=3, padding=1)(latent)
        outputs.append(x)


        x = ResBlock(80)([x, t_emb])
        x = SpatialTransformer(2, 40, fully_connected=False)([x, context])
        outputs.append(x)
        x = PaddedConv2D(80, 3, strides=2, padding=1)(x)  # Downsample 2x
        outputs.append(x)

        x = ResBlock(160)([x, t_emb])
        x = SpatialTransformer(4, 40, fully_connected=False)([x, context])
        outputs.append(x)
        x = PaddedConv2D(160, 3, strides=2, padding=1)(x)  # Downsample 2x
        outputs.append(x)

        x = ResBlock(320)([x, t_emb])
        x = SpatialTransformer(4, 80, fully_connected=False)([x, context])
        outputs.append(x)
        x = PaddedConv2D(320, 3, strides=2, padding=1)(x)  # Downsample 2x
        outputs.append(x)

        x = ResBlock(320)([x, t_emb])
        outputs.append(x)

        # Middle flow

        x = ResBlock(320)([x, t_emb])
        x = SpatialTransformer(4, 80, fully_connected=False)([x, context])
        x = ResBlock(320)([x, t_emb])

        # Upsampling flow

        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(320)([x, t_emb])
        # x = Upsample(320)(x)

        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(320)([x, t_emb])
        x = SpatialTransformer(4, 80, fully_connected=False)([x, context])
        x = Upsample(320)(x)

        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(320)([x, t_emb])
        x = SpatialTransformer(4, 80, fully_connected=False)([x, context])
        # x = Upsample(320)(x)

        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(160)([x, t_emb])
        x = SpatialTransformer(4, 40, fully_connected=False)([x, context])
        x = Upsample(160)(x)

        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(160)([x, t_emb])
        x = SpatialTransformer(4, 40, fully_connected=False)([x, context])

        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(80)([x, t_emb])
        x = SpatialTransformer(2, 40, fully_connected=False)([x, context])
        x = Upsample(160)(x)

        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(80)([x, t_emb])
        x = SpatialTransformer(2, 40, fully_connected=False)([x, context])

        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(80)([x, t_emb])
        x = SpatialTransformer(2, 40, fully_connected=False)([x, context])

        # # Exit flow

        x = keras.layers.GroupNormalization(groups=20, epsilon=1e-5)(x)
        x = keras.layers.Activation("swish")(x)
        output = PaddedConv2D(4, kernel_size=3, padding=1)(x)


        super().__init__([latent, t_embed_input, context], output, name=name)




#%%
class MicroDiffusionModel(k.Model):
    def __init__(self, img_height=128, img_width=128, nr_channels=1, max_text_length=100, name=None):
        
        context = keras.layers.Input((max_text_length, 768))
        t_embed_input = keras.layers.Input((320,))
        latent = keras.layers.Input((img_height // 8, img_width // 8, nr_channels))

        t_emb = keras.layers.Dense(320)(t_embed_input)
        t_emb = keras.layers.Activation("swish")(t_emb)
        t_emb = keras.layers.Dense(320)(t_emb)

        # Downsampling flow

        outputs = []

        x = PaddedConv2D(40, kernel_size=3, padding=1)(latent)
        outputs.append(x)

        x = ResBlock(40)([x, t_emb])
        x = SpatialTransformer(2, 20, fully_connected=False)([x, context])
        outputs.append(x)
        x = PaddedConv2D(40, 3, strides=2, padding=1)(x)  # Downsample 2x
        outputs.append(x)

        x = ResBlock(80)([x, t_emb])
        x = SpatialTransformer(4, 20, fully_connected=False)([x, context])
        outputs.append(x)
        x = PaddedConv2D(80, 3, strides=2, padding=1)(x)  # Downsample 2x
        outputs.append(x)

        x = ResBlock(160)([x, t_emb])
        x = SpatialTransformer(4, 40, fully_connected=False)([x, context])
        outputs.append(x)
        x = PaddedConv2D(160, 3, strides=2, padding=1)(x)  # Downsample 2x
        outputs.append(x)

        # Middle flow

        x = ResBlock(160)([x, t_emb])
        x = SpatialTransformer(4, 40, fully_connected=False)([x, context])
        x = ResBlock(160)([x, t_emb])

        # Upsampling flow

        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(160)([x, t_emb])
        x = SpatialTransformer(4, 40, fully_connected=False)([x, context])
        x = Upsample(160)(x)
        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(160)([x, t_emb])
        x = SpatialTransformer(4, 40, fully_connected=False)([x, context])

        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(80)([x, t_emb])
        x = SpatialTransformer(4, 20, fully_connected=False)([x, context])
        x = Upsample(80)(x)
        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(80)([x, t_emb])
        x = SpatialTransformer(4, 20, fully_connected=False)([x, context])

        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(40)([x, t_emb])
        x = SpatialTransformer(2, 20, fully_connected=False)([x, context])
        x = Upsample(80)(x)
        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(40)([x, t_emb])
        x = SpatialTransformer(2, 20, fully_connected=False)([x, context])

        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(40)([x, t_emb])
        x = SpatialTransformer(2, 20, fully_connected=False)([x, context])

        # # Exit flow

        x = keras.layers.GroupNormalization(groups=20, epsilon=1e-5)(x)
        x = keras.layers.Activation("swish")(x)
        output = PaddedConv2D(4, kernel_size=3, padding=1)(x)


        super().__init__([latent, t_embed_input, context], output, name=name)



#%%
class NanoDiffusionModel(k.Model):
    def __init__(self, img_height=128, img_width=128, nr_channels=1, max_text_length=100, name=None):
        
        context = keras.layers.Input((max_text_length, 768))
        t_embed_input = keras.layers.Input((320,))
        latent = keras.layers.Input((img_height // 8, img_width // 8, nr_channels))

        t_emb = keras.layers.Dense(320)(t_embed_input)
        t_emb = keras.layers.Activation("swish")(t_emb)
        t_emb = keras.layers.Dense(320)(t_emb)

        # Downsampling flow

        outputs = []

        x = PaddedConv2D(40, kernel_size=3, padding=1)(latent)
        outputs.append(x)

        x = ResBlock(40)([x, t_emb])
        x = SpatialTransformer(2, 20, fully_connected=False)([x, context])
        outputs.append(x)
        x = PaddedConv2D(40, 3, strides=2, padding=1)(x)  # Downsample 2x
        outputs.append(x)

        x = ResBlock(80)([x, t_emb])
        x = SpatialTransformer(4, 20, fully_connected=False)([x, context])
        outputs.append(x)
        x = PaddedConv2D(80, 3, strides=2, padding=1)(x)  # Downsample 2x
        outputs.append(x)


        # Middle flow

        x = ResBlock(80)([x, t_emb])
        x = SpatialTransformer(4, 20, fully_connected=False)([x, context])
        x = ResBlock(80)([x, t_emb])

        # Upsampling flow

        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(80)([x, t_emb])
        x = SpatialTransformer(4, 20, fully_connected=False)([x, context])
        x = Upsample(80)(x)
        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(80)([x, t_emb])
        x = SpatialTransformer(4, 20, fully_connected=False)([x, context])

        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(40)([x, t_emb])
        x = SpatialTransformer(2, 20, fully_connected=False)([x, context])
        x = Upsample(80)(x)
        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(40)([x, t_emb])
        x = SpatialTransformer(2, 20, fully_connected=False)([x, context])

        x = keras.layers.Concatenate()([x, outputs.pop()])
        x = ResBlock(40)([x, t_emb])
        x = SpatialTransformer(2, 20, fully_connected=False)([x, context])

        # # Exit flow

        x = keras.layers.GroupNormalization(groups=20, epsilon=1e-5)(x)
        x = keras.layers.Activation("swish")(x)
        output = PaddedConv2D(4, kernel_size=3, padding=1)(x)


        super().__init__([latent, t_embed_input, context], output, name=name)





# %%
k.backend.clear_session()

model = MiniDiffusionModel(128, 128, 1, 100)

# %%
