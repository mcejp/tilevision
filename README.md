Usage example:

    tilevision-run my_kernel.py

Example kernel:

```python
from tilevision.matplotlib_util import bg_from_heightmap
from tilevision.path_util import circle, line, line_polar, polyline, rectangle_centered, star, triangle
from tilevision.tilevision import Label, Path


logger = logging.getLogger(__name__)


class MyKernel:
    # OPTIONAL
    @staticmethod
    def register_args(parser):
        parser.add_argument("--version", required=True, type=int, choices=[2018, 2021])

    def __init__(self, args, tv):
        tv.send_hello(w=world_size[0],
                      h=world_size[1],
                      bg=bg_from_heightmap(world_height, vmin=-200, vmax=1000))

    @property
    def name(self):
        return f"Settlements 2021"

    def report(self, f):
        for settlement in self._settlements:
            f.write(f'~settlement:~ `{settlement.name:31s}`\n')
            f.write(f'~houses:~     `{len(settlement.houses)    :4d}` | ~houses needed:~    `{housing_need:3d}`\n')
            f.write(f'~population:~ `{len(settlement.people)    :4d}` | ~food consumption:~ `{yearly_food_consumption:3d}`/yr\n')
            f.write(f'~farmland:~   `{farmable_tiles            :4d}` | ~food yield:~       `{yearly_farm_yield:3d}`/yr\n')
            f.write(f'~food:~       `{settlement.food_reserves:4.0f}` | ~net gain:~         `{yearly_farm_yield - yearly_food_consumption:3d}`/yr\n')
            f.write("\n")

    def step(self, tv):
        labels = []
        paths = []

        for x1, y1, x2, y2 in self._road_network['road_segments']:
            paths.append(Path(line(x1, y1, x2, y2),
                              linedash=[0.4, 0.15],
                              linewidth=0.2,
                              stroke="rgba(255,255,255,0.8)"))

        for x, y in np.ndindex(self._world_height.shape):
            def draw_field(x, y):
                return " ".join(circle(x + xx * 0.5 - 0.25, y + yy * 0.5 - 0.25, 0.1) for xx, yy in np.ndindex((2, 2)))

            def draw_house(x, y):
                return polyline([(x - 0.3, y - 0.4),
                                 (x + 0.3, y - 0.4),
                                 (x + 0.3, y),
                                 (x + 0.5, y),
                                 (x,       y + 0.5),
                                 (x - 0.5, y),
                                 (x - 0.3, y),
                                 ])

            if self._building_faction[x, y] != 0:
                paths.append(Path(draw_house(x, y), fill="rgba(255,255,255,0.6)"))
            if farm_faction[x, y] != 0:
                paths.append(Path(draw_field(x, y), linewidth=0.1, fill="rgba(255,255,255,0.8)"))
            elif self._farmable[x, y] != 0:
                paths.append(Path(rectangle_centered(x, y, 0.45, 0.45), linewidth=0.1, stroke="rgba(255,255,255,0.25)"))

        for settlement in self._settlements:
            x = settlement.x
            y = settlement.y
            labels.append(Label(x + 0.5, y - 1.5,
                                f'{settlement.name} ({len(settlement.people)})',
                                color="#ffffff", fontsize=1.5))
            paths.append(Path(star(5, r1=0.7, r2=0.3, x=x, y=y), fill="#ffffff"))

        tv.send_annotations(labels, paths)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    from tilevision.runner import run_kernel
    run_kernel(MyKernel)

```
