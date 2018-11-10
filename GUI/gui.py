import kivy

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.theming import ThemeManager

from Map.map_manager import plot_map

kivy.require('1.10.1')

main_widget_kv = '''
#:import get_color_from_hex kivy.utils
#:import Toolbar kivymd.toolbar.Toolbar
#:import ThemeManager kivymd.theming.ThemeManager
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import NavigationDrawerDivider kivymd.navigationdrawer.NavigationDrawerDivider
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar
#:import NavigationDrawerSubheader kivymd.navigationdrawer.NavigationDrawerSubheader
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox
#:import MDSwitch kivymd.selectioncontrols.MDSwitch
#:import MDList kivymd.list.MDList
#:import OneLineListItem kivymd.list.OneLineListItem
#:import TwoLineListItem kivymd.list.TwoLineListItem
#:import ThreeLineListItem kivymd.list.ThreeLineListItem
#:import OneLineAvatarListItem kivymd.list.OneLineAvatarListItem
#:import OneLineIconListItem kivymd.list.OneLineIconListItem
#:import OneLineAvatarIconListItem kivymd.list.OneLineAvatarIconListItem
#:import MDTextField kivymd.textfields.MDTextField
#:import MDSpinner kivymd.spinner.MDSpinner
#:import MDCard kivymd.card.MDCard
#:import MDSeparator kivymd.card.MDSeparator
#:import MDDropdownMenu kivymd.menu.MDDropdownMenu
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import colors kivymd.color_definitions.colors
#:import SmartTile kivymd.grid.SmartTile
#:import MDSlider kivymd.slider.MDSlider
#:import MDTabbedPanel kivymd.tabs.MDTabbedPanel
#:import MDTab kivymd.tabs.MDTab
#:import MDProgressBar kivymd.progressbar.MDProgressBar
#:import MDAccordion kivymd.accordion.MDAccordion
#:import MDAccordionItem kivymd.accordion.MDAccordionItem
#:import MDAccordionSubItem kivymd.accordion.MDAccordionSubItem
#:import MDThemePicker kivymd.theme_picker.MDThemePicker
#:import MDBottomNavigation kivymd.tabs.MDBottomNavigation
#:import MDBottomNavigationItem kivymd.tabs.MDBottomNavigationItem
#:import CEFBrowser kivy.garden.cefpython
#:import MDFlatButton kivymd.button
#:import MDCheckbox kivymd.selectioncontrols

NavigationLayout:
    id: nav_layout
    MDNavigationDrawer:
        id: nav_drawer
        NavigationDrawerToolbar:
            title: "GroupFinder"
        NavigationDrawerIconButton:
            icon: 'code-braces'
            text: 'Clustering'
            on_release: app.root.ids.scr_mngr.current = 'clustering'
        NavigationDrawerIconButton:
            icon: 'map-marker'
            text: "Map"
            on_release: app.root.ids.scr_mngr.current = 'map_scr'
        NavigationDrawerIconButton:
            icon: 'settings'
            text: "Settings"
            on_release: app.root.ids.scr_mngr.current = 'settings'
    BoxLayout:
        orientation: 'vertical'
        Toolbar:
            id: toolbar
            title: 'GroupFinder'
            md_bg_color: app.theme_cls.primary_color
            background_palette: 'Primary'
            background_hue: '500'
            left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
        ScreenManager:
            id: scr_mngr
            Screen:
                name: 'clustering'
            Screen:
                name: 'map_scr'
                CEFBrowser:
                    id: map_view
                    url: "file:///Map/map.html"
            Screen:
                name: 'settings'
                ScrollView:
                    do_scroll_x: False
                    MDList:
                        id: theme_setting_list
                        MDLabel:
                            padding_x: dp(15)
                            id: label_theme
                            font_style: 'Body2'
                            theme_text_color: 'Custom'
                            text_color: app.theme_cls.primary_color
                            text: "Theme settings"
                            valign: 'middle'
                            size_hint_y: None
                            height: self.texture_size[1] + dp(4)
                        TwoLineListItem:
                            text: "Dark theme"
                            secondary_text: "Enable dark theme throughout the app"
                            on_release: dark_mode_slider.trigger_action()
                            MDSwitch:
                                id: dark_mode_slider
                                size_hint: None, None
                                size: dp(24), dp(31)
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(40)
                                active: False
                                callback: app.change_theme(self.active)
                        TwoLineListItem:
                            text: "Theme color"
                            secondary_text: "Change theme color"
                            MDIconButton:
                                id: blue_theme_button
                                value: "blue"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Blue").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(40)*9
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: orange_theme_button
                                value: "orange"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Orange").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(40)*8
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: green_theme_button
                                value: "green"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Green").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(40)*7
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: red_theme_button
                                value: "red"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Red").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(40)*6
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: brown_theme_button
                                value: "brown"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Brown").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(40)*5
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: purple_theme_button
                                value: "purple"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Purple").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(40)*4
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: yellow_theme_button
                                value: "yellow"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Amber").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(40)*3
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: pink_theme_button
                                value: "pink"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Pink").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(40)*2
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: teal_theme_button
                                value: "teal"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Teal").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(40)
                                on_press: app.change_theme_color(self.value)
                        TwoLineListItem:
                            text: "Use OpenStreetMap"
                            secondary_text: "Use maps from OpenStreetMap"
                            on_release: osm_check.trigger_action()
                            MDCheckbox:
                                id: osm_check
                                size_hint: None, None
                                size: dp(24), dp(31)
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(40)
                                active: False
                                callback: app.set_open_street_maps(self.active)
'''


class GroupFinderApp(App):
    data = None
    map_view = None
    map = None
    osm = False
    theme_cls = ThemeManager()
    window_width = 1024
    window_height = 576
    Window.size = (window_width, window_height)

    def set_open_street_maps(self, value):
        theme = ""
        if value:
            self.osm = True
        else:
            self.osm = False
            if self.theme_cls.theme_style is 'Dark':
                theme = "dark"
            elif self.theme_cls.theme_style is 'Light':
                theme = "light"
        self.map = plot_map(theme, self.osm)
        if self.map_view is not None:
            self.map_view.reload()

    def change_theme(self, active):
        if active:
            self.theme_cls.theme_style = 'Dark'
            self.map = plot_map("dark", self.data)
            if self.map_view is not None and self.osm is False:
                self.map_view.reload()
        else:
            self.theme_cls.theme_style = 'Light'
            self.map = plot_map("light", self.data)
            if self.map_view is not None and self.osm is False:
                self.map_view.reload()

    def change_theme_color(self, color):
        if color is "blue":
            self.theme_cls.primary_palette = "Blue"
            self.theme_cls.accent_palette = "Amber"
        if color is "orange":
            self.theme_cls.primary_palette = "Orange"
            self.theme_cls.accent_palette = "LightBlue"
        if color is "green":
            self.theme_cls.primary_palette = "Green"
            self.theme_cls.accent_palette = "Red"
        if color is "red":
            self.theme_cls.primary_palette = "Red"
            self.theme_cls.accent_palette = "Orange"
        if color is "brown":
            self.theme_cls.primary_palette = "Brown"
            self.theme_cls.accent_palette = "Green"
        if color is "purple":
            self.theme_cls.primary_palette = "Purple"
            self.theme_cls.accent_palette = "Amber"
        if color is "yellow":
            self.theme_cls.primary_palette = "Amber"
            self.theme_cls.accent_palette = "Cyan"
        if color is "pink":
            self.theme_cls.primary_palette = "Pink"
            self.theme_cls.accent_palette = "LightBlue"
        if color is "teal":
            self.theme_cls.primary_palette = "Teal"
            self.theme_cls.accent_palette = "Yellow"

    def build(self):
        main_widget = Builder.load_string(main_widget_kv)
        self.map = plot_map("light")
        self.map_view = main_widget.ids.map_view
        return main_widget
