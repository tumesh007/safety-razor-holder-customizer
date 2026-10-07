"""
FreeCAD & VTK Studio Product Renderer
Produces high-resolution photorealistic PBR renders without GPU dependency.
"""

import os
import math
import vtk

def create_studio_renderer():
    """Create a studio renderer with 4-point studio lighting and luxury gradient backdrop."""
    renderer = vtk.vtkRenderer()
    
    # Soft luxury studio gradient background
    renderer.SetBackground(0.96, 0.97, 0.98)   # Clean studio top
    renderer.SetBackground2(0.80, 0.83, 0.87)  # Subtle shadow vignette bottom
    renderer.SetGradientBackground(True)
    
    # 1. Key Light (Soft warm main light, 45 deg front-right)
    key_light = vtk.vtkLight()
    key_light.SetPosition(300, -320, 280)
    key_light.SetFocalPoint(30, 0, 50)
    key_light.SetColor(1.0, 0.98, 0.95)
    key_light.SetIntensity(1.15)
    renderer.AddLight(key_light)
    
    # 2. Fill Light (Cool diffuse fill to balance high contrast)
    fill_light = vtk.vtkLight()
    fill_light.SetPosition(-320, -180, 180)
    fill_light.SetFocalPoint(30, 0, 50)
    fill_light.SetColor(0.88, 0.93, 1.0)
    fill_light.SetIntensity(0.55)
    renderer.AddLight(fill_light)
    
    # 3. Rim / Edge Light (Behind and above to illuminate silhouette fillets)
    rim_light = vtk.vtkLight()
    rim_light.SetPosition(0, 320, 260)
    rim_light.SetFocalPoint(30, 0, 50)
    rim_light.SetColor(1.0, 1.0, 1.0)
    rim_light.SetIntensity(0.85)
    renderer.AddLight(rim_light)
    
    # 4. Soft Bottom / Undercut Bounce
    bounce_light = vtk.vtkLight()
    bounce_light.SetPosition(20, -100, -150)
    bounce_light.SetFocalPoint(30, 0, 30)
    bounce_light.SetColor(0.95, 0.96, 0.98)
    bounce_light.SetIntensity(0.35)
    renderer.AddLight(bounce_light)
    
    return renderer

def load_stl_actor(stl_path, color_rgb=(0.14, 0.16, 0.20), roughness=0.32, metallic=0.0):
    """Load STL and construct actor with PBR materials and smooth feature normals."""
    reader = vtk.vtkSTLReader()
    reader.SetFileName(stl_path)
    reader.Update()
    
    normals = vtk.vtkPolyDataNormals()
    normals.SetInputConnection(reader.GetOutputPort())
    normals.SetFeatureAngle(42.0)
    normals.ComputePointNormalsOn()
    normals.ComputeCellNormalsOn()
    normals.SplittingOn()
    normals.Update()
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(normals.GetOutputPort())
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    
    prop = actor.GetProperty()
    if hasattr(prop, 'SetInterpolationToPBR'):
        prop.SetInterpolationToPBR()
        prop.SetRoughness(roughness)
        prop.SetMetallic(metallic)
    else:
        prop.SetInterpolationToPhong()
        prop.SetSpecular(0.4)
        prop.SetSpecularPower(30.0)
        
    prop.SetColor(*color_rgb)
    prop.SetAmbient(0.18)
    prop.SetDiffuse(0.82)
    
    return actor

def render_scene(actors, output_path, cam_pos, cam_focal, cam_up=(0, 0, 1),
                 resolution=(1920, 1080), zoom=1.0, extra_lights=None):
    """Render actors into high-resolution offscreen PNG with antialiasing."""
    renderer = create_studio_renderer()
    for act in actors:
        renderer.AddActor(act)
        
    if extra_lights:
        for lt in extra_lights:
            renderer.AddLight(lt)
            
    camera = renderer.GetActiveCamera()
    camera.SetPosition(*cam_pos)
    camera.SetFocalPoint(*cam_focal)
    camera.SetViewUp(*cam_up)
    renderer.ResetCameraClippingRange()
    if zoom != 1.0:
        camera.Zoom(zoom)
        
    renWin = vtk.vtkRenderWindow()
    renWin.SetOffScreenRendering(1)
    renWin.AddRenderer(renderer)
    renWin.SetSize(*resolution)
    renWin.SetMultiSamples(8) # 8x MSAA
    
    renWin.Render()
    
    w2if = vtk.vtkWindowToImageFilter()
    w2if.SetInput(renWin)
    w2if.SetInputBufferTypeToRGB()
    w2if.ReadFrontBufferOff()
    w2if.Update()
    
    writer = vtk.vtkPNGWriter()
    writer.SetFileName(output_path)
    writer.SetInputConnection(w2if.GetOutputPort())
    writer.Write()
    print(f"Rendered: {output_path}")

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(root, "docs", "images")
    os.makedirs(output_dir, exist_ok=True)
    
    model_upright = os.path.join(root, "models", "30mm", "Halter_30mm_Tumesh_Upright.stl")
    model_flatside = os.path.join(root, "models", "30mm", "Halter_30mm_Tumesh.stl")
    model_custom = os.path.join(root, "customize_holder.stl")
    if not os.path.exists(model_custom):
        model_custom = model_upright
        
    print("=== Generating Studio Renders with FreeCAD VTK ===")
    
    # 1. Hero 3/4 Isometric Studio Shot
    print("1/4: Rendering Hero Studio Shot...")
    hero_actor = load_stl_actor(model_upright, color_rgb=(0.14, 0.16, 0.20), roughness=0.32)
    render_scene(
        actors=[hero_actor],
        output_path=os.path.join(output_dir, "render_hero_studio.png"),
        cam_pos=(280, -320, 180),
        cam_focal=(30, 0, 68),
        cam_up=(0, 0, 1),
        zoom=0.95
    )
    
    # 2. Angled Top-Down Overview (Razor, Brush knot, Soap Bowl)
    print("2/4: Rendering Top Functional Overview...")
    top_actor = load_stl_actor(model_upright, color_rgb=(0.14, 0.16, 0.20), roughness=0.32)
    render_scene(
        actors=[top_actor],
        output_path=os.path.join(output_dir, "render_top_overview.png"),
        cam_pos=(100, -260, 320),
        cam_focal=(30, 0, 60),
        cam_up=(0, 0, 1),
        zoom=0.92
    )
    
    # 3. Bottom Branding Showcase (Debossed name & emblem)
    print("3/4: Rendering Bottom Branding Detail...")
    branding_actor = load_stl_actor(model_custom, color_rgb=(0.20, 0.22, 0.27), roughness=0.26)
    b_light1 = vtk.vtkLight()
    b_light1.SetPosition(80, -220, -140)
    b_light1.SetFocalPoint(30, 0, 0)
    b_light1.SetIntensity(1.3)
    
    b_light2 = vtk.vtkLight()
    b_light2.SetPosition(-80, 80, -180)
    b_light2.SetFocalPoint(30, 0, 0)
    b_light2.SetIntensity(0.5)
    
    render_scene(
        actors=[branding_actor],
        output_path=os.path.join(output_dir, "render_bottom_branding.png"),
        cam_pos=(30, -150, -190),
        cam_focal=(30, 0, 0),
        cam_up=(0, -0.8, 0.6),
        zoom=1.45,
        extra_lights=[b_light1, b_light2]
    )
    
    # 4. Flat-Side Fast-Print Bed Orientation (Simulated PEI Plate)
    print("4/4: Rendering Flat-Side Bed Adhesion View...")
    flat_actor = load_stl_actor(model_flatside, color_rgb=(0.14, 0.16, 0.20), roughness=0.32)
    
    plane = vtk.vtkPlaneSource()
    plane.SetOrigin(-60, -90, -0.2)
    plane.SetPoint1(160, -90, -0.2)
    plane.SetPoint2(-60, 110, -0.2)
    plane.Update()
    
    p_mapper = vtk.vtkPolyDataMapper()
    p_mapper.SetInputConnection(plane.GetOutputPort())
    p_actor = vtk.vtkActor()
    p_actor.SetMapper(p_mapper)
    p_prop = p_actor.GetProperty()
    if hasattr(p_prop, 'SetInterpolationToPBR'):
        p_prop.SetInterpolationToPBR()
        p_prop.SetRoughness(0.55)
        p_prop.SetMetallic(0.1)
    p_prop.SetColor(0.24, 0.23, 0.22)
    
    render_scene(
        actors=[p_actor, flat_actor],
        output_path=os.path.join(output_dir, "render_flatside_bed.png"),
        cam_pos=(220, -260, 150),
        cam_focal=(35, 5, 25),
        cam_up=(0, 0, 1),
        zoom=1.30
    )
    
    print("=== All Renders Successfully Generated ===")

if __name__ == "__main__":
    main()
