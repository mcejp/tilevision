import matplotlib
import matplotlib.pyplot


def bg_from_heightmap(hmap, vmin, vmax):
    sm = matplotlib.cm.ScalarMappable(matplotlib.colors.Normalize(vmin=vmin, vmax=vmax),
                                      matplotlib.pyplot.get_cmap('gist_earth'))

    bg = []

    for y in range(hmap.shape[1]):
        for x in range(hmap.shape[0]):
            rgba = sm.to_rgba(hmap[x, y])
            r, g, b = int(rgba[0] * 255), int(rgba[1] * 255), int(rgba[2] * 255)
            bg.append(f"#{r:02x}{g:02x}{b:02x}")

    return bg
