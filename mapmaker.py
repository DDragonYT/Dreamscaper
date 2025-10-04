import flet as ft
import json
import os
import keyboard

global map_obj
global map_items
global paint_brush
map_obj = {}
map_items = []
map_layer = 0
paint_brush = 0

def main(page: ft.Page):
    def load_map(e):
        global map_obj
        global map_layer
        display_columns = [ft.Column(spacing=0, scroll=ft.ScrollMode.ALWAYS) for x in range(4)]
        if os.path.exists(rf"maps\{map_name.value}.json"):
            with open(rf"maps\{map_name.value}.json", "r") as mapjson:
                map_obj = json.load(mapjson)
                update_map()
        else:
            map_obj["height"],map_obj["width"] = int(map_height.value),int(map_width.value)
            for x in range(0,3):
                map_obj[f"layer{x}"] = [int(base_input.value) if x == 0 else 1 for _ in range(int(map_height.value)*int(map_width.value))]
            save_map(e)
            update_map()

    def tile_hovered(e:ft.ControlEvent):
        if keyboard.is_pressed("e"):
            tile_clicked(e)

    def tile_clicked(e:ft.ControlEvent):
        global paint_brush
        global map_obj
        global map_layer
        global map_items
        i = e.control.data
        map_obj[f"layer{map_layer}"][i] = int(paint_brush)
        map_items[map_layer][i].content.src = rf"tiles\{paint_brush}.png"
        page.update()

    def update_map():
        global map_obj
        global map_items
        map_items = []
        map_width = map_obj["width"]
        for layer in range(0,3):
            map_items.append([])
            display_columns[layer].controls.clear()
            blocklist = map_obj[f"layer{layer}"]
            i = 0
            while i != len(blocklist):
                new_row = ft.Row(spacing=0)
                for x in range(map_width):
                    map_items[layer].append(ft.Container(
                        ft.Image(
                            src=(
                                rf"tiles/{blocklist[i]}.png"
                                if os.path.exists(rf"tiles/{blocklist[i]}.png")
                                else r"tiles/0.png"
                            ),
                            width=16,
                            height=16,
                        ),
                        ink = True if layer == 2 else None,
                        on_click=tile_clicked if layer == 2 else None,
                        on_hover=tile_hovered if layer == 2 else None,
                        data= i,
                        ink_color= ft.Colors.WHITE
                    ))
                    new_row.controls.append(map_items[layer][i])
                    i += 1
                display_columns[layer].controls.insert(0, new_row)
        page.update()

    def layer_clicked(e):
        global map_layer
        map_layer = int(e.control.data) if e.control.data != "all" else e.control.data
        if e.control.data == "all":
            for layer in display_stack.controls:
                layer.visible = True
                layer.opacity = 1
            page.update()
        else:
            for i in range(0,3):
                if i <= e.control.data:
                    display_columns[i].opacity = 1
                    if i != e.control.data:
                        display_columns[i].opacity = 0.5-(0.1*(e.control.data-i))
                else:
                    display_columns[i].opacity = 0.25           
            page.update()
    
    def save_map(e):
        global map_obj
        json.dump(map_obj, open(rf"maps\{map_name.value}.json","w+"))
    

    def pallette_clicked(e):
        global paint_brush
        paint_brush,_ = e.control.data

    save_button = ft.Button("Save", on_click= save_map)
    locr_button = ft.Button("Load/Create", on_click=load_map)
    map_name = ft.TextField("maps",width=150)
    map_height = ft.TextField(30, width=60)
    map_width = ft.TextField(30, width=60)
    base_input = ft.TextField(26, width=40)

    display_columns = [ft.Column(spacing=0, scroll=ft.ScrollMode.ALWAYS) for x in range(4)]
    display_stack = ft.Stack(display_columns)
    layer_row = ft.Row([ft.CupertinoButton(text= f"{x}",on_click=layer_clicked, data=x) for x in [0,1,2,3,"all"]])
    pallette = ft.Container(ft.GridView(
        controls=[
            ft.Container(
                        ft.Image(
                            src=
                                rf"tiles/{file}"
                                if os.path.exists(rf"tiles/{file}")
                                else r"tiles/0.png"
                            ,
                            width=64,
                            height=64,
                            scale=2,
                            
                        ),
                        on_click=pallette_clicked,
                        data=os.path.splitext(file),
                        ink=True,
                    )
            for file in os.listdir("tiles")

        ],
        runs_count=5,
        spacing=3,
        run_spacing=3,
        
    ),
    width=200,
    height=page.window.height-200)

    display_container = ft.Container(
        ft.InteractiveViewer(
            min_scale=0.1,
            max_scale=15,
            trackpad_scroll_causes_scale=True,
            content=display_stack,
            
        ),
        width=page.window.width - 300,
        height=page.window.height - 200,
        bgcolor=ft.Colors.GREY_800
    )



    page.add(
        ft.Row(
            [
                ft.Text("Map name: "),
                map_name,
                ft.Text("Height: "),
                map_height,
                ft.Text("Width: "),
                map_width,
                ft.Text("Base: "),
                base_input,
                locr_button,
                save_button,
                ft.Text("               Layers:"),
                layer_row
            ],scale=0.8
        ),
        ft.Row([display_container,pallette]),
    )





ft.app(main, ft.AppView.FLET_APP)
