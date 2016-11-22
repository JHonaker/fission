from Render import RenderComponent, RenderSystem
from Position import PositionComponent
from EntityManager import EntityManager
from SystemManager import SystemManager
import tdl

em = EntityManager()
em.createEntity()
em.createEntity()
p1 = PositionComponent(1, 1)
em.addComponentTo(0, p1)
em.addComponentTo(0, RenderComponent("@", (255, 255, 255), (0, 0, 0)))
em.addComponentTo(1, PositionComponent(1, 2))
em.addComponentTo(1, RenderComponent("#", (255, 100, 100), (0, 0, 0)))

sm = SystemManager(em)
sm.addSystem(RenderSystem(sm._entityManager, sm))

while not tdl.event.is_window_closed():
    sm.update(0)
    p1.x = (p1.x + 1) % 5
