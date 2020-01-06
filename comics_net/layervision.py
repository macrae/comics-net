"Layer visualization of Comics Net models"

import random

import matplotlib.pyplot as plt
import numpy as np
import torch
from IPython.display import clear_output
from torch import Tensor, tensor


def init_pixel_buf(size: int, cuda: bool = False, seed=None) -> Tensor:
    """Initialize a pixel buffer.

    Args:
        size (int): Size of buffer

    Returns:
        Tensor: Pixel buffer
    """
    if seed is not None:
        np.random.seed(seed)

    img_buf = torch.empty(1, 3, size, size).normal_(mean=0, std=0.01)

    if cuda:
        img_buf = torch.sigmoid(tensor(img_buf)).cuda()
    else:
        img_buf = torch.sigmoid(tensor(img_buf))

    return img_buf


def init_fft_buf(size: int, sd: float = 0.01, cuda: bool = False, seed=None) -> Tensor:
    """Initialize a Discrete Fourier Transform buffer.

    Args:
        size (int): Size of buffer

    Returns:
        Tensor: Discrete Fourier Transform buffer
    """
    if seed is not None:
        np.random.seed(seed)

    # size => output shape; scale => standard deviation of gaussian distribution
    img_buf = np.random.normal(size=(1, 3, size, size // 2 + 1, 2), scale=sd).astype(
        np.float32
    )

    if cuda:
        spectrum_t = tensor(img_buf).float().cuda()
    else:
        spectrum_t = tensor(img_buf).float()

    return spectrum_t


def fft_to_rgb(
    t: Tensor,
    d: float = 0.5,
    decay_power: int = 1,
    cuda: bool = False,
    seed=None,
    **kwargs,
) -> Tensor:
    """Transform a Discrete Fourier Transform to an RGB object.

    Args:
        t: Tensor to transform
        d (optional): Sample spacing (inverse of the sampling rate). Defaults to 0.5.
        decay_power (optional): Applies to scale rate. Defaults to 1.

    Returns:
        Tensor: ...
    """
    if seed is not None:
        np.random.seed(seed)

    size = t.shape[-3]

    fy = np.fft.fftfreq(size, d=d)[:, None]
    fx = np.fft.fftfreq(size, d=d)[: size // 2 + 1]
    freqs = np.sqrt(fx * fx + fy * fy)
    scale = 1.0 / np.maximum(freqs, 1.0 / size) ** decay_power
    if cuda:
        scale = tensor(scale).float()[None, None, ..., None].cuda()
    else:
        scale = tensor(scale).float()[None, None, ..., None]
    scale *= size
    t = scale * t

    image_t = torch.irfft(t, signal_ndim=2, signal_sizes=(size, size))
    image_t = image_t / 4.0

    return image_t


def lucid_to_rgb(t: Tensor, cuda: bool = False, seed=None) -> Tensor:
    """Decorrelate color of an RGB tensor.

    Args:
        t (Tensor): Tensor to decorrelate

    Returns:
        Tensor: Decorrelated tensor
    """
    if seed is not None:
        np.random.seed(seed)

    color_correlation_svd_sqrt = np.asarray(
        [[0.26, 0.09, 0.02], [0.27, 0.00, -0.05], [0.27, -0.09, 0.03]]
    ).astype(np.float32)
    max_norm_svd_sqrt = np.max(np.linalg.norm(color_correlation_svd_sqrt, axis=0))

    t_flat = t.permute(0, 2, 3, 1)

    if cuda:
        color_correlation_normalized = tensor(
            color_correlation_svd_sqrt / max_norm_svd_sqrt
        ).cuda()
    else:
        color_correlation_normalized = tensor(
            color_correlation_svd_sqrt / max_norm_svd_sqrt
        )

    t_flat = torch.matmul(t_flat, color_correlation_normalized.T)
    t = t_flat.permute(0, 3, 1, 2)
    return t


def image_buf_to_rgb(
    img_buf: Tensor, jitter: float, decorrelate=True, fft=True, **kwargs
) -> Tensor:
    """Transform an image buffer to RGB buffer

    Args:
        img_buf (Tensor): Image buffer to transform
        jitter (float): Amount to jitter pixel locations by
        decorrelate (bool, optional): ???. Defaults to True.
        fft (bool, optional): ???. Defaults to True.

    Returns:
        Tensor: Transformed RGB tensor
    """
    img = img_buf.detach()
    if fft:
        img = fft_to_rgb(img, **kwargs)
    size = img.shape[-1]
    x_off, y_off = jitter // 2, jitter // 2
    if decorrelate:
        img = lucid_to_rgb(img)
    img = torch.sigmoid(img)
    img = img[
        :, :, x_off : x_off + size - jitter, y_off : y_off + size - jitter
    ]  # jitter
    img = img.squeeze()
    return img


def show_rgb(img: Tensor, label=None, ax=None, dpi=25, **kwargs) -> None:
    """Plot an image.

    Args:
        img (Tensor): [description]
        label ([type], optional): [description]. Defaults to None.
        ax ([type], optional): [description]. Defaults to None.
        dpi (int, optional): [description]. Defaults to 25.
    """
    plt_show = True if ax == None else False
    if ax == None:
        _, ax = plt.subplots(figsize=(img.shape[1] / dpi, img.shape[2] / dpi))
    x = img.cpu().permute(1, 2, 0).numpy()
    ax.imshow(x)
    ax.axis("off")
    ax.set_title(label)
    if plt_show:
        plt.show()


def visualize_feature(
    model,
    layer,
    feature,
    size=200,
    jitter=25,
    steps=2000,
    lr=0.05,
    decorrelate=True,
    fft=True,
    debug=False,
    frames=10,
    show=True,
    **kwargs,
):
    img_buf = init_fft_buf(size + jitter) if fft else init_pixel_buf(size + jitter)
    img_buf.requires_grad_()
    opt = torch.optim.Adam([img_buf], lr=lr)

    hook_out = None

    def callback(m, i, o):
        nonlocal hook_out
        hook_out = o

    hook = layer.register_forward_hook(callback)

    for i in range(1, steps + 1):
        x_off, y_off = (
            int(np.random.random() * jitter),
            int(np.random.random() * jitter),
        )
        img = fft_to_rgb(img_buf, **kwargs) if fft else img_buf
        img = img[:, :, x_off : x_off + size + 1, y_off : y_off + size + 1]  # jitter
        if decorrelate:
            img = lucid_to_rgb(img)  # decorrelate color
        model(img.cuda())
        opt.zero_grad()
        loss = -1 * hook_out[0][feature].mean()
        loss.backward()
        opt.step()
        if debug and (i) % (steps / frames) == 0:
            clear_output(wait=True)
            show_rgb(
                image_buf_to_rgb(
                    img_buf, jitter, decorrelate=decorrelate, fft=fft, **kwargs
                ),
                label=f"step: {i} loss: {loss}",
                **kwargs,
            )

    hook.remove()

    retval = image_buf_to_rgb(
        img_buf, jitter, decorrelate=decorrelate, fft=fft, **kwargs
    )
    if show:
        if not debug:
            show_rgb(retval, **kwargs)
    else:
        return retval
