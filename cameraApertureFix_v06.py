# cameraApertureFix v06
# Copyright (c) 2024 Giuseppe Pagnozzi
#
# This script is provided freely and generously.
# You can use, study, modify, and share it.
# It's licensed under the MIT License
# visit https://opensource.org/licenses/MIT for the full terms.

import maya.cmds as cmds
import traceback

PRESETS = {
    "65mm Film (5-perf)": {"horizontal": 48.56, "vertical": 22.1, "unit": "mm"},
    "Arri Alexa 65": {"horizontal": 54.12, "vertical": 25.59, "unit": "mm"},
    "Arri Alexa Classic (16:9)": {"horizontal": 23.76, "vertical": 13.365, "unit": "mm"},
    "Arri Alexa LF (Open Gate)": {"horizontal": 36.7, "vertical": 25.54, "unit": "mm"},
    "Arri Alexa Mini (16:9)": {"horizontal": 23.76, "vertical": 13.365, "unit": "mm"},
    "Arri Alexa Mini LF (Open Gate)": {"horizontal": 36.7, "vertical": 25.54, "unit": "mm"},
    "APS-C (Canon)": {"horizontal": 22.3, "vertical": 14.9, "unit": "mm"},
    "APS-C (Sony/Nikon/Fujifilm)": {"horizontal": 23.6, "vertical": 15.6, "unit": "mm"},
    "Blackmagic Pocket 6K (Super 35)": {"horizontal": 23.1, "vertical": 12.99, "unit": "mm"},
    "Blackmagic Pocket 4K (MFT)": {"horizontal": 18.96, "vertical": 10.0, "unit": "mm"},
    "Canon C300 Mark III (Super 35)": {"horizontal": 26.2, "vertical": 13.8, "unit": "mm"},
    "Full Frame 35mm (Photography)": {"horizontal": 36.0, "vertical": 24.0, "unit": "mm"},
    "IMAX 70mm (15-perf)": {"horizontal": 70.41, "vertical": 52.63, "unit": "mm"},
    "Maya (Default Camera)": {"horizontal": 36.0, "vertical": 24.0, "unit": "mm"},
    "Micro Four Thirds": {"horizontal": 17.3, "vertical": 13.0, "unit": "mm"},
    "RED Dragon (6K Full)": {"horizontal": 30.7, "vertical": 15.8, "unit": "mm"},
    "RED Komodo (6K S35)": {"horizontal": 26.21, "vertical": 13.82, "unit": "mm"},
    "Sony FX3/A7S III": {"horizontal": 35.6, "vertical": 23.8, "unit": "mm"},
    "Sony Venice (6K Full)": {"horizontal": 36.2, "vertical": 24.1, "unit": "mm"},
    "Standard 16mm Film": {"horizontal": 10.26, "vertical": 7.49, "unit": "mm"},
    "Standard 35mm Film (Academy)": {"horizontal": 22.0, "vertical": 16.0, "unit": "mm"},
    "Super 16mm Film": {"horizontal": 12.52, "vertical": 7.41, "unit": "mm"},
    "Super 35mm Film": {"horizontal": 24.89, "vertical": 18.67, "unit": "mm"},
}

def create_camera_tool_ui():
    current_data = {
        'camera_shape': None, 'camera_transform': None,
        'aperture': 0.0, 'vertical_aperture': 0.0,
        'initial_aspect_ratio': 1.0, 'focal_length': 0.0,
        'unit': 'Inch', 'maintain_aspect_ratio': True,
        'preset_active': False, 'selected_preset_name': None,
        'adjust_focal_length': True
    }

    selected = cmds.ls(selection=True)
    if selected and cmds.listRelatives(selected[0], shapes=True, type='camera'):
        camera_transform = selected[0]
        camera_shape = cmds.listRelatives(camera_transform, shapes=True, type='camera')[0]
        try:
            current_data.update({
                'camera_shape': camera_shape,
                'camera_transform': camera_transform,
                'aperture': cmds.getAttr(camera_shape + ".horizontalFilmAperture"),
                'vertical_aperture': cmds.getAttr(camera_shape + ".verticalFilmAperture"),
                'focal_length': cmds.getAttr(camera_shape + ".focalLength")
            })
            if current_data['vertical_aperture'] != 0:
                current_data['initial_aspect_ratio'] = current_data['aperture'] / current_data['vertical_aperture']
            else:
                current_data['initial_aspect_ratio'] = 1.0
        except Exception as e:
            print(f"Initial load: Error reading attributes from {camera_shape}: {e}")
            current_data.update({'camera_shape': None, 'camera_transform': None})

    if cmds.window("cameraToolWin", exists=True):
        cmds.deleteUI("cameraToolWin")

    window = cmds.window("cameraToolWin", title="CameraApertureFix v06", widthHeight=(400, 430), sizeable=True)
    scroll_layout = cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnOffset=["both", 10])

    cmds.text(label="Camera Info", font="boldLabelFont", align="left")
    cmds.columnLayout(adjustableColumn=True, rowSpacing=2)
    current_camera_text = cmds.text(label="Camera: N/A")
    current_focal_length_text = cmds.text(label="Focal Length: N/A")
    current_aperture_text = cmds.text(label="Horiz Film Aperture: N/A")
    current_vertical_aperture_text = cmds.text(label="Vert Film Aperture: N/A")
    cmds.setParent("..")

    cmds.separator(height=10, style="in")

    cmds.text(label="Settings", font="boldLabelFont", align="left")
    settings_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=5)

    cmds.rowLayout(numberOfColumns=2, columnAttach=[(1, 'both', 5), (2, 'both', 5)])
    preset_menu = cmds.optionMenu(
        label="Presets", en=False,
        annotation="Select a camera preset. 'None' enables manual input."
    )
    cmds.menuItem(label="None")
    for preset_name_iter in PRESETS.keys(): cmds.menuItem(label=preset_name_iter)
    unit_menu = cmds.optionMenu(
        label="Unit", en=False,
        annotation="Choose the unit for aperture display and input (Inch or mm)."
    )
    cmds.menuItem(label="Inch")
    cmds.menuItem(label="mm")
    cmds.setParent("..")

    cmds.rowLayout(numberOfColumns=2, columnWidth2=(180, 100))
    cmds.text(label="Horizontal Film Aperture")
    new_aperture_field = cmds.floatField(
        precision=6, en=False,
        annotation="Enter new horizontal aperture. Enabled if 'None' preset is selected."
    )
    cmds.setParent("..")

    cmds.rowLayout(numberOfColumns=2, columnWidth2=(180, 100))
    cmds.text(label="Vertical Film Aperture")
    new_vertical_aperture_field = cmds.floatField(
        precision=6, en=False,
        annotation="Enter new vertical aperture. Enabled if 'Maintain Aspect Ratio' is OFF and 'None' preset is selected."
    )
    cmds.setParent("..")

    maintain_aspect_check = cmds.checkBox(
        label="Maintain Original Aspect Ratio", en=False,
        annotation="Checked: Vertical aperture is automatically calculated to preserve the aspect ratio of the camera *as currently loaded/refreshed in this tool*.\nUnchecked (with Preset): Uses both Horizontal & Vertical apertures from the selected preset, which may alter the aspect ratio.\nUnchecked (with 'None' Preset): Enables manual input for Vertical Film Aperture, allowing you to define a custom aspect ratio."
    )
    adjust_fl_check = cmds.checkBox(
        label="Adjust Focal Length to Maintain FOV", en=False,
        annotation="Checked: Focal length is adjusted to maintain field of view relative to horizontal aperture change.\nUnchecked: Focal length remains unchanged."
    )
    cmds.setParent("..") 

    cmds.text(label="Preview of Calculated Changes:", font="smallBoldLabelFont", align='left', parent=main_layout)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=2, columnOffset=["left", 10], parent=main_layout)
    preview_h_ap_text = cmds.text(label="New Horiz Aperture: N/A", align='left')
    preview_v_ap_text = cmds.text(label="New Vert Aperture: N/A", align='left')
    preview_aspect_text = cmds.text(label="New Aspect Ratio: N/A", align='left')
    preview_fl_text = cmds.text(label="New Focal Length: N/A", align='left')
    cmds.setParent("..")

    cmds.rowLayout(numberOfColumns=2, columnAttach=[(1, 'both', 5), (2, 'both', 5)], parent=main_layout)
    apply_button = cmds.button(
        label="Apply", en=False,
        annotation="Applies the specified aperture settings and adjusts focal length if enabled."
    )
    reset_button = cmds.button(
        label="Reset", en=False,
        annotation="Resets all settings and reloads data from the selected camera."
    )
    cmds.setParent("..")

    cmds.separator(height=10, style="in", parent=main_layout)

    cmds.rowLayout(numberOfColumns=2, columnAttach=[(1, 'both', 5), (2, 'both', 5)], parent=main_layout)
    refresh_button = cmds.button(
        label="Refresh",
        annotation="Reloads data from the currently selected camera in the Maya scene."
    )
    cmds.button(label="Close", command=lambda *args: cmds.deleteUI(window))
    cmds.setParent("..")

    cmds.setParent("..")

    cmds.optionMenu(preset_menu, edit=True, changeCommand=lambda *args: apply_preset())
    cmds.optionMenu(unit_menu, edit=True, changeCommand=lambda *args: update_unit_and_fields())
    cmds.floatField(new_aperture_field, edit=True, changeCommand=lambda *args: update_new_focal_length(True))
    cmds.floatField(new_vertical_aperture_field, edit=True, changeCommand=lambda *args: update_new_focal_length(True))
    cmds.checkBox(maintain_aspect_check, edit=True, changeCommand=lambda value: update_maintain_aspect(value))
    cmds.checkBox(adjust_fl_check, edit=True, changeCommand=lambda value: update_adjust_focal_length(value))
    cmds.button(apply_button, edit=True, command=lambda *args: apply_new_focal_length())
    cmds.button(reset_button, edit=True, command=lambda *args: reset_inputs())
    cmds.button(refresh_button, edit=True, command=lambda *args: refresh())
    
    def manage_vfa_field_state():
        if not current_data['camera_shape']:
            cmds.floatField(new_vertical_aperture_field, edit=True, enable=False, value=0.0)
            return

        vfa_field_enabled = (
            not current_data['maintain_aspect_ratio'] and
            not current_data['preset_active']
        )
        cmds.floatField(new_vertical_aperture_field, edit=True, enable=vfa_field_enabled)

        if vfa_field_enabled:
            display_v_ap = convert_aperture(current_data['vertical_aperture'], current_data['unit'])
            cmds.floatField(new_vertical_aperture_field, edit=True, value=display_v_ap)

    def update_maintain_aspect(value):
        current_data['maintain_aspect_ratio'] = value
        update_data_and_ui()

    def update_adjust_focal_length(value):
        current_data['adjust_focal_length'] = value
        update_new_focal_length()

    def convert_aperture(aperture_inches, to_unit):
        if to_unit == "Inch": return aperture_inches
        elif to_unit == "mm": return aperture_inches * 25.4
        return aperture_inches

    def convert_to_inches(aperture_value, from_unit):
        if from_unit == "Inch": return aperture_value
        elif from_unit == "mm": return aperture_value / 25.4
        return aperture_value

    def _prompt_for_refresh():
        cmds.confirmDialog(title="Refresh Required", message="Camera selection may have changed or is out of sync. Please press 'Refresh'.", button=['OK'], defaultButton='OK', icon='warning')

    def _check_selection_matches_data():
        stored_cam_transform = current_data.get('camera_transform')
        if not stored_cam_transform:
            selected_check = cmds.ls(selection=True)
            if selected_check and cmds.listRelatives(selected_check[0], shapes=True, type='camera'):
                return False
            return True
        
        selected_check = cmds.ls(selection=True)
        if not selected_check or not cmds.listRelatives(selected_check[0], shapes=True, type='camera'):
            if stored_cam_transform: 
                return False
            return True 

        return selected_check[0] == stored_cam_transform

    def update_unit_and_fields():
        if not current_data['camera_shape'] : return
        
        current_data['unit'] = cmds.optionMenu(unit_menu, query=True, value=True)
        update_data_and_ui()

    def apply_preset():
        if not current_data['camera_shape']: return

        preset_name_val = cmds.optionMenu(preset_menu, query=True, value=True)
        current_data['selected_preset_name'] = preset_name_val
        current_data['preset_active'] = (preset_name_val != "None" and preset_name_val in PRESETS)
        
        update_data_and_ui()

    def refresh_camera_info_display():
        if not current_data['camera_shape']:
            cmds.text(current_camera_text, e=1, l="Camera: Please select a camera and press refresh.")
            cmds.text(current_focal_length_text, e=1, l="Focal Length: N/A")
            cmds.text(current_aperture_text, e=1, l="Horiz Film Aperture: N/A")
            cmds.text(current_vertical_aperture_text, e=1, l="Vert Film Aperture: N/A")
            return

        cmds.text(current_camera_text, e=1, l=f"Camera: {current_data['camera_transform']}")
        cmds.text(current_focal_length_text, e=1, l=f"Focal Length: {current_data['focal_length']:.4f} mm")
        
        hfa_inch = current_data['aperture']
        vfa_inch = current_data['vertical_aperture']
        hfa_mm = hfa_inch * 25.4
        vfa_mm = vfa_inch * 25.4
        cmds.text(current_aperture_text, e=1, l=f"Horiz Film Aperture: {hfa_inch:.4f} Inch ({hfa_mm:.3f} mm)")
        cmds.text(current_vertical_aperture_text, e=1, l=f"Vert Film Aperture: {vfa_inch:.4f} Inch ({vfa_mm:.3f} mm)")

    def update_data_and_ui():
        has_camera = bool(current_data['camera_shape'])

        cmds.optionMenu(preset_menu, e=1, en=has_camera)
        cmds.optionMenu(unit_menu, e=1, en=has_camera)
        cmds.floatField(new_aperture_field, e=1, en=(has_camera and not current_data['preset_active']))
        cmds.checkBox(maintain_aspect_check, e=1, en=has_camera, v=current_data['maintain_aspect_ratio'])
        cmds.checkBox(adjust_fl_check, e=1, en=has_camera, v=current_data['adjust_focal_length'])
        cmds.button(apply_button, e=1, en=has_camera)
        cmds.button(reset_button, e=1, en=has_camera)

        refresh_camera_info_display()

        if has_camera:
            hfa_source_inches = current_data['aperture']
            if current_data['preset_active']:
                preset_h_mm = PRESETS[current_data['selected_preset_name']].get("horizontal", 0.0)
                hfa_source_inches = convert_to_inches(preset_h_mm, "mm")
            cmds.floatField(new_aperture_field, e=1, v=convert_aperture(hfa_source_inches, current_data['unit']))

            manage_vfa_field_state() 
            
            cmds.checkBox(maintain_aspect_check, e=1, v=current_data['maintain_aspect_ratio'])
            cmds.checkBox(adjust_fl_check, e=1, v=current_data['adjust_focal_length'])
            cmds.optionMenu(unit_menu, e=1, v=current_data['unit'])
            if current_data['selected_preset_name'] and current_data['selected_preset_name'] != "None":
                 cmds.optionMenu(preset_menu, e=1, v=current_data['selected_preset_name'])
            else:
                 cmds.optionMenu(preset_menu, e=1, sl=1) 

        else: 
            cmds.floatField(new_aperture_field, e=1, v=0.0)
            cmds.floatField(new_vertical_aperture_field, e=1, v=0.0, en=False)
            cmds.optionMenu(preset_menu, e=1, sl=1)

        update_new_focal_length()

    def update_new_focal_length(manual_trigger=False):
        if manual_trigger and not _check_selection_matches_data():
            _prompt_for_refresh()
            for PTV, PPL in [(preview_h_ap_text, "New Horiz Aperture"), (preview_v_ap_text, "New Vert Aperture"), 
                             (preview_aspect_text, "New Aspect Ratio"), (preview_fl_text, "New Focal Length")]:
                if cmds.text(PTV, q=1, ex=1): cmds.text(PTV, e=1, l=f"{PPL}: (Refresh!)")
            if cmds.button(apply_button, q=1, ex=1): cmds.button(apply_button, e=1, en=False)
            return

        if not current_data['camera_shape']:
            for PTV, PPL in [(preview_h_ap_text, "New Horiz Aperture"), (preview_v_ap_text, "New Vert Aperture"), 
                             (preview_aspect_text, "New Aspect Ratio"), (preview_fl_text, "New Focal Length")]:
                if cmds.text(PTV, q=1, ex=1): cmds.text(PTV, e=1, l=f"{PPL}: N/A")
            if cmds.button(apply_button, q=1, ex=1): cmds.button(apply_button, e=1, en=False)
            return
        
        try:
            new_h_aperture_display_unit = cmds.floatField(new_aperture_field, query=True, value=True)
            new_h_aperture_in_inches = convert_to_inches(new_h_aperture_display_unit, current_data['unit'])

            can_apply_hfa = new_h_aperture_in_inches > 0
            if not can_apply_hfa:
                if cmds.text(preview_h_ap_text, q=1, ex=1): cmds.text(preview_h_ap_text, e=1, l="New Horiz Aperture: Invalid (>0)")

            preview_v_ap_inch = 0.0
            vfa_manual_mode_active = (not current_data['maintain_aspect_ratio'] and
                                      not current_data['preset_active'])
            can_apply_vfa = True 

            if current_data['maintain_aspect_ratio']:
                preview_v_ap_inch = new_h_aperture_in_inches / current_data['initial_aspect_ratio'] if current_data['initial_aspect_ratio'] != 0 else 0
            elif current_data['preset_active']:
                preset_v_mm = PRESETS[current_data['selected_preset_name']].get("vertical", 0.0)
                preview_v_ap_inch = convert_to_inches(preset_v_mm, "mm")
            elif vfa_manual_mode_active:
                v_ap_display_unit = cmds.floatField(new_vertical_aperture_field, query=True, value=True)
                preview_v_ap_inch = convert_to_inches(v_ap_display_unit, current_data['unit'])
                can_apply_vfa = preview_v_ap_inch > 0
                if not can_apply_vfa:
                     if cmds.text(preview_v_ap_text, q=1, ex=1): cmds.text(preview_v_ap_text, e=1, l="New Vert Aperture: Invalid (>0)")
            else: 
                preview_v_ap_inch = current_data['vertical_aperture']
            
            if not vfa_manual_mode_active or can_apply_vfa : 
                cmds.floatField(new_vertical_aperture_field, e=1, v=convert_aperture(preview_v_ap_inch, current_data['unit']))

            preview_aspect_ratio = new_h_aperture_in_inches / preview_v_ap_inch if preview_v_ap_inch > 0 else float('inf')
            fl_preview_label = "New Focal Length: Error"

            if current_data['adjust_focal_length']:
                if new_h_aperture_in_inches > 0 and current_data['aperture'] > 0:
                    scale_factor = current_data['aperture'] / new_h_aperture_in_inches
                    calculated_fl = current_data['focal_length'] / scale_factor
                    fl_preview_label = f"New Focal Length: {calculated_fl:.3f} mm"
                elif new_h_aperture_in_inches > 0:
                    fl_preview_label = f"New Focal Length: {current_data['focal_length']:.3f} mm (Orig HFA 0)"
                else: 
                    fl_preview_label = "New Focal Length: Invalid HFA"
            else:
                fl_preview_label = f"Focal Length: {current_data['focal_length']:.3f} mm (Unchanged)"

            if can_apply_hfa:
                cmds.text(preview_h_ap_text, e=1, l=f"New Horiz Aperture: {new_h_aperture_in_inches:.4f} Inch ({convert_aperture(new_h_aperture_in_inches, 'mm'):.3f} mm)")
            if can_apply_vfa or not vfa_manual_mode_active: 
                 cmds.text(preview_v_ap_text, e=1, l=f"New Vert Aperture: {preview_v_ap_inch:.4f} Inch ({convert_aperture(preview_v_ap_inch, 'mm'):.3f} mm)")
            
            cmds.text(preview_aspect_text, e=1, l=f"New Aspect Ratio: {preview_aspect_ratio:.4f}")
            cmds.text(preview_fl_text, e=1, l=fl_preview_label)
            
            if cmds.button(apply_button, q=1, ex=1): cmds.button(apply_button, e=1, en=(can_apply_hfa and can_apply_vfa))

        except Exception as e_update:
            print(f"Error during preview update: {e_update}")
            traceback.print_exc()
            for PTV, PPL in [(preview_h_ap_text, "Horiz Aperture"), (preview_v_ap_text, "Vert Aperture"), 
                             (preview_aspect_text, "Aspect Ratio"), (preview_fl_text, "Focal Length")]:
                if cmds.text(PTV, q=1, ex=1): cmds.text(PTV, e=1, l=f"New {PPL}: Error")
            if cmds.button(apply_button, q=1, ex=1): cmds.button(apply_button, e=1, en=False)

    def apply_new_focal_length():
        if not _check_selection_matches_data(): _prompt_for_refresh(); return
        if not current_data['camera_shape']: cmds.warning("No camera selected."); return

        cmds.undoInfo(openChunk=True)
        try:
            h_ap_display = cmds.floatField(new_aperture_field, q=1, v=1)
            applied_h_ap_inches = convert_to_inches(h_ap_display, current_data['unit'])

            if applied_h_ap_inches <= 0:
                cmds.warning("Horizontal Aperture must be positive."); cmds.undoInfo(closeChunk=True); return
            
            cmds.setAttr(current_data['camera_shape'] + ".horizontalFilmAperture", applied_h_ap_inches)
            
            applied_v_ap_inches = current_data['vertical_aperture'] 
            vfa_manual_mode = (not current_data['maintain_aspect_ratio'] and
                               not current_data['preset_active'])

            if current_data['maintain_aspect_ratio']:
                applied_v_ap_inches = applied_h_ap_inches / current_data['initial_aspect_ratio'] if current_data['initial_aspect_ratio'] != 0 else current_data['vertical_aperture']
            elif current_data['preset_active']:
                preset_v_mm = PRESETS[current_data['selected_preset_name']].get("vertical", 0.0)
                applied_v_ap_inches = convert_to_inches(preset_v_mm, "mm")
            elif vfa_manual_mode:
                v_ap_display = cmds.floatField(new_vertical_aperture_field, q=1, v=1)
                manual_v_ap_inches = convert_to_inches(v_ap_display, current_data['unit'])
                if manual_v_ap_inches > 0:
                    applied_v_ap_inches = manual_v_ap_inches
                else:
                     cmds.warning("Manual Vertical Aperture was invalid (<=0). VFA not changed from camera's current value.")

            if applied_v_ap_inches > 0:
                 cmds.setAttr(current_data['camera_shape'] + ".verticalFilmAperture", applied_v_ap_inches)
            else: 
                print(f"Warning: Final vertical aperture value ({applied_v_ap_inches}) is invalid. Not setting.")


            if current_data['adjust_focal_length']:
                original_hfa_for_fl_calc = current_data['aperture'] 
                if applied_h_ap_inches > 0 and original_hfa_for_fl_calc > 0:
                    scale_factor_fl = original_hfa_for_fl_calc / applied_h_ap_inches
                    if abs(scale_factor_fl - 1.0) > 1e-6: 
                        focal_attr = current_data['camera_shape'] + ".focalLength"
                        original_fl = current_data['focal_length'] 
                        new_fl = original_fl / scale_factor_fl
                        
                        anim_curves = cmds.listConnections(focal_attr, type="animCurve", scn=True)
                        if anim_curves:
                            cmds.scaleKey(anim_curves, valueScale=(1.0/scale_factor_fl), valuePivot=0)
                        else:
                            cmds.setAttr(focal_attr, new_fl)
            
            refresh(force_reload_from_scene=True)

        except Exception as e_apply:
            cmds.warning(f"Error applying changes: {e_apply}")
            traceback.print_exc()
        finally:
            cmds.undoInfo(closeChunk=True)

    def reset_inputs():
        if not current_data['camera_shape']: cmds.warning("No camera selected."); return
        
        current_data.update({
            'unit': 'Inch', 'maintain_aspect_ratio': True,
            'preset_active': False, 'selected_preset_name': "None", 
            'adjust_focal_length': True
        })
        refresh(force_reload_from_scene=True)

    def refresh(force_reload_from_scene=False):
        selected_refresh = cmds.ls(selection=True)
        cam_data_loaded_this_refresh = False
        new_cam_shape = None
        new_cam_transform = None

        if selected_refresh and cmds.listRelatives(selected_refresh[0], shapes=True, type='camera'):
            new_cam_transform = selected_refresh[0]
            new_cam_shape = cmds.listRelatives(new_cam_transform, shapes=True, type='camera')[0]
        
        if new_cam_shape and (new_cam_shape != current_data.get('camera_shape') or force_reload_from_scene):
            try:
                current_data.update({
                    'camera_shape': new_cam_shape, 'camera_transform': new_cam_transform,
                    'aperture': cmds.getAttr(new_cam_shape + ".horizontalFilmAperture"),
                    'vertical_aperture': cmds.getAttr(new_cam_shape + ".verticalFilmAperture"),
                    'focal_length': cmds.getAttr(new_cam_shape + ".focalLength")
                })
                current_data['initial_aspect_ratio'] = current_data['aperture'] / current_data['vertical_aperture'] if current_data['vertical_aperture'] != 0 else 1.0
                cam_data_loaded_this_refresh = True
            except Exception as e_refresh:
                print(f"Refresh: Error reading attributes from {new_cam_shape}: {e_refresh}")
                current_data.update({'camera_shape': None, 'camera_transform': None}) 
        elif new_cam_shape and new_cam_shape == current_data.get('camera_shape') and not force_reload_from_scene:
            cam_data_loaded_this_refresh = True
        elif not new_cam_shape: 
             current_data.update({'camera_shape': None, 'camera_transform': None})


        current_data['preset_active'] = False
        current_data['selected_preset_name'] = "None"
        current_data['maintain_aspect_ratio'] = True
        current_data['adjust_focal_length'] = True
        
        update_data_and_ui()

    cmds.optionMenu(unit_menu, e=1, v=current_data['unit'])
    
    cmds.showWindow(window)
    refresh(force_reload_from_scene=True)

if __name__ == "__main__":
    create_camera_tool_ui()
