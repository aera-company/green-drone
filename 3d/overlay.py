"""Render de silhueta na câmera resolvida + overlay vermelho sobre o master."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene, drone_model
sol = json.load(open(os.path.join(scene.OUT, "camera_refined.json")))["cam"]
extra = json.loads(scene.args()[0]) if scene.args() else {}
scene.reset()
drone_model.build({"s": sol["s"], "spoke_phase": sol["phase"], **extra}, silhouette=True)
scene.workbench_silhouette()
scene.size(1000, 667)
scene.camera(sol["az"], sol["el"], sol["dist"], sol["focal"], (sol["tx"], sol["ty"], sol["tz"]), sol["roll"])
scene.render_to(os.path.join(scene.OUT, "_sil.png"))
