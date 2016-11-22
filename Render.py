from Component import Component
from Position import PositionComponent
from System import System
import tdl


class RenderComponent(Component):

    def __init__(self, glyph, fg, bg):
        self.glyph = glyph
        self.fg = fg
        self.bg = bg


class RenderSystem(System):

    def __init__(self, entityManager, systemManager):
        super().__init__(entityManager, systemManager,
                         requiredComponents=(RenderComponent,
                                             PositionComponent))

        screenWidth = 80
        screenHeight = 50
        limitFps = 5
        print("Creating Console")
        self._console = tdl.init(screenWidth, screenHeight,
                                 title="RL-ECS", fullscreen=False)

        tdl.setFPS(limitFps)

    def update(self, delta):
        self._console.clear()
        for e, compDict in self.components().items():
            position = compDict[PositionComponent]
            render = compDict[RenderComponent]
            self._console.draw_char(position.x, position.y,
                                    render.glyph,
                                    fg=render.fg,
                                    bg=render.bg)
        tdl.flush()
