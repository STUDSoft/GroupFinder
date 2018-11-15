import kivy

import threading

import tkinter as tk
from tkinter import filedialog
import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder

from kivy.uix.scrollview import ScrollView

from kivymd.bottomsheet import MDListBottomSheet
from kivymd.theming import ThemeManager

from Map.map_manager import plot_map, add_users_positions

from kivy.utils import get_color_from_hex
from kivy.animation import Animation

from Algorithms.dataset_parser import get_dataset
from Algorithms.staypoint_detector import staypoint_detection
from Algorithms.clustering import hdbscan_clust
from Algorithms.sequence_manager import extract_sequencies, calculate_similarities

from kivymd.snackbar import Snackbar
from kivymd.label import MDLabel
from kivymd.dialog import MDDialog
from kivymd.list import MDList, OneLineListItem
from kivymd.selectioncontrols import MDCheckbox

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
#:import MDDropdownMenu kivymd.menu.MDMenuItem
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
#:import MDTextField kivymd.textfields
#:import MDFloatingActionButton kivymd.button
#:import MDCard kivymd.card


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
                id: clustering
                name: 'clustering'
                ScrollView:
                    do_scroll_x: False
                    BoxLayout:
                        id: clustering_settings
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        padding: 20
                        spacing: 5
                        MDLabel:
                            font_style: 'Body2'
                            theme_text_color: 'Custom'
                            text_color: app.theme_cls.primary_color
                            text: "Clustering options"
                        BoxLayout:
                            size_hint_y: None
                            height: 10
                            orientation: 'horizontal'
                        GridLayout:
                            cols: 2
                            size_hint: (None, None)
                            row_force_default: True
                            row_default_height: self.minimum_height
                            width: self.parent.width - 25
                            height: self.minimum_height
                            GridLayout:
                                rows: 2
                                row_force_default: True
                                row_default_height: 20
                                MDLabel:
                                    font_style: 'Subhead'
                                    theme_text_color: 'Primary'
                                    text: "Dataset file"
                                MDLabel:
                                    font_style: 'Body1'
                                    theme_text_color: 'Secondary'
                                    text: "Select dataset file"
                            MDFlatButton:
                                id: dataset_file
                                text: "Add file"
                                on_press: app.choose_file()
                                theme_text_color: 'Custom'
                                text_color: app.theme_cls.primary_color
                        BoxLayout:
                            size_hint_y: None
                            orientation: 'horizontal'
                            width: self.parent.width
                            height: 5
                            MDLabel:
                                id: file_error
                                theme_text_color: "Custom"
                                text_color: get_color_from_hex("D50000")
                                halign: "right"
                        MDTextField:
                            name: "dist_thresh"
                            id: dist_thresh
                            on_text_validate: app.set_error(self)
                            hint_text: "Distance threshold in meters necessary to consider two points as in the same staypoint (default is 200 meters)" 
                            helper_text: ""
                            helper_text_mode: "on_error"
                        MDTextField:
                            name: "time_thresh"
                            id: time_thresh
                            on_text_validate: app.set_error(self)
                            hint_text: "Time threshold in minutes necessary to consider two points as in the same staypoint (default is 30 minutes)" 
                            helper_text: ""
                            helper_text_mode: "on_error"
                        MDTextField:
                            name: "min_pts"
                            id: min_pts
                            on_text_validate: app.set_error(self)
                            hint_text: "Number of minimum points needed to create a cluster (default is 2 points)" 
                            helper_text: ""
                            helper_text_mode: "on_error"
                        MDTextField:
                            name: "max_length"
                            id: max_length
                            on_text_validate: app.set_error(self)
                            hint_text: "Max length of a similar sequence (default is 4 points)" 
                            helper_text: ""
                            helper_text_mode: "on_error"
                        MDTextField:
                            name: "eps"
                            id: eps
                            on_text_validate: app.set_error(self)
                            hint_text: "Time constraint in minutes that denotes two similar transition times between the same region (default is 10 minutes)" 
                            helper_text: ""
                            helper_text_mode: "on_error"
                MDFloatingActionButton:
                    id: cluster_button
                    elevation_normal: 9
                    center_x: root.width - 45
                    center_y: 45
                    icon: 'magnify'
                    on_press: app.start_clustering()
            Screen:
                id: map_scr
                name: 'map_scr'
                CEFBrowser:
                    id: map_view
                    url: "file:///Map/map.html"
                MDCard:
                    id: users_card
                    size: self.parent.width, self.parent.height
                    border_radius: dp(10)
                    y: -self.height + 45
                    BoxLayout:
                        id: layout_user
                        orientation:'vertical'
                        padding: dp(20), dp(4), dp(20), dp(4)
                        spacing: 5
                        MDLabel:
                            text: 'Title'
                            theme_text_color: 'Primary'
                            font_style:"Title"
                            size_hint_y: None
                            height: dp(36)
                            halign: "center"
                        MDLabel:
                            id: label_no_users
                            font_style: "Body1"
                            theme_text_color: 'Primary'
                            halign: "center"
                        GridLayout:
                            cols: 3
                            size_hint_y: None
                            height: dp(15)
                            MDSlider:
                                id: hslider
                                min:0
                                max:100
                                value: 80
                                size_hint_x: 0.8
                                halign: "center"
                            MDLabel:
                                text: "Min. similarity:"
                                font_style: "Body1"
                                theme_text_color: 'Primary'           
                                size_hint_x: 0.15
                                halign: "center"
                            MDLabel:
                                text: "{0:.1f}".format(hslider.value)
                                font_style: "Body1"
                                theme_text_color: 'Primary'            
                                size_hint_x: 0.05
                                halign: "left"
                        ScrollView:
                            do_scroll_x: False
                            MDList:
                                id: user_list
                MDFloatingActionButton:
                    id: users_button
                    elevation_normal: 9
                    center_x: root.width - 45
                    center_y: 45
                    icon: 'arrow-up'
                    on_release: app.show_users_menu()                        
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
                            secondary_text: "Enable dark theme throughout the app (will reset the map)"
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
                                center_x: self.parent.width - dp(35)*9
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: orange_theme_button
                                value: "orange"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Orange").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(35)*8
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: green_theme_button
                                value: "green"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Green").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(35)*7
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: red_theme_button
                                value: "red"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Red").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(35)*6
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: brown_theme_button
                                value: "brown"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Brown").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(35)*5
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: purple_theme_button
                                value: "purple"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Purple").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(35)*4
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: yellow_theme_button
                                value: "yellow"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Amber").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(35)*3
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: pink_theme_button
                                value: "pink"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Pink").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(35)*2
                                on_press: app.change_theme_color(self.value)
                            MDIconButton:
                                id: teal_theme_button
                                value: "teal"
                                icon: 'checkbox-blank-circle'
                                theme_text_color: 'Custom'
                                text_color: get_color_from_hex(colors.get("Teal").get(app.theme_cls.primary_hue))
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(35)
                                on_press: app.change_theme_color(self.value)
                        TwoLineListItem:
                            text: "Use OpenStreetMap"
                            secondary_text: "Use maps from OpenStreetMap that are more detailed in terms of restaurants, places etc. (will reset the map)"
                            on_release: osm_check.trigger_action()
                            MDCheckbox:
                                id: osm_check
                                size_hint: None, None
                                size: dp(31), dp(31)
                                center_y: self.parent.center_y
                                center_x: self.parent.width - dp(35)
                                active: False
                                callback: app.set_open_street_maps(self.active)
        FloatLayout:
            size_hint: None, None
            size: 0, 0
            MDCard:
                id: card
                size_hint: None, None
                height: dp(45)
                width: dp(300)
                center_x: root.width/2
                center_y: -35
                border_radius: dp(10)
                BoxLayout:
                    id: clust_progress
                    padding: 12
                    spacing: 20
                    MDSpinner:
                        id: spinner
                        size_hint: None, None
                        pos_hint: {'center_y': 0.5}
                        size: dp(25), dp(25)
                    MDLabel:
                        id: clustering_label
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
'''


class GroupFinderApp(App):
    data = None
    map = None
    osm = False
    dataset_file = None
    file_label = None
    map_view = None
    file_error = None
    card = None
    clust_progress = None
    clustering_label = None

    dist_thresh = 200
    time_thresh = 30
    min_pts = 2
    max_length = 4
    eps = 10

    user_card_opened = False
    can_press = True

    num_sp_per_user = None
    userlist = None
    sp = None
    staypoints = None
    clusterer = None
    sequencies = None
    similarities = None
    map_scr = None
    users_button = None
    user_list = None
    users_card = None
    label_user = None
    layout_user = None

    theme_cls = ThemeManager()
    window_width = 1024
    window_height = 576
    Window.size = (window_width, window_height)

    def set_error(self, tf):
        value = tf.text
        try:
            value = int(value)
            if value < 0:
                tf.helper_text = "Insert a positive number"
                tf.error = True
            elif value is 0:
                tf.helper_text = "Insert a number different than 0"
                tf.error = True
            else:
                tf.helper_text = ""
                tf.error = False
                if tf.name is "dist_thresh":
                    self.dist_thresh = value
                elif tf.name is "time_thresh":
                    self.time_thresh = value
                elif tf.name is "min_pts":
                    self.min_pts = value
                elif tf.name is "max_length":
                    self.max_length = value
                elif tf.name is "eps":
                    self.eps = value
        except ValueError:
            if value is "":
                tf.helper_text = ""
                if tf.name is "dist_thresh":
                    self.dist_thresh = 200
                elif tf.name is "time_thresh":
                    self.time_thresh = 30
                elif tf.name is "min_pts":
                    self.min_pts = 2
                elif tf.name is "max_length":
                    self.max_length = 4
                elif tf.name is "eps":
                    self.eps = 10
            else:
                tf.helper_text = "Insert a number"
                tf.error = True

    def worker(self):
        animation = Animation(center_y=40, duration=0.25)
        animation.start(self.card)

        self.clustering_label.text = "Extracting dataset"
        self.userlist = get_dataset(self.dataset_file)

        self.layout_user.remove_widget(self.label_user)
        self.user_list.clear_widgets()

        self.clustering_label.text = "Detecting staypoints"
        self.sp, self.staypoints, self.num_sp_per_user = staypoint_detection(self.userlist, self.dist_thresh, self.time_thresh)

        self.clustering_label.text = "HDBSCAN clustering going on"
        self.clusterer = hdbscan_clust(self.sp, self.min_pts, 'haversine')

        self.clustering_label.text = "Extracting sequencies"
        self.sequencies = extract_sequencies(self.staypoints, self.clusterer.labels_.tolist())

        self.clustering_label.text = "Calculating similarities"
        self.similarities = calculate_similarities(self.sequencies, self.num_sp_per_user,
                                                   self.max_length,
                                                   self.eps)

        self.clustering_label.text = "Building map"
        self.map = add_users_positions(self.map, self.userlist)
        self.map_view.reload()

        for u in self.userlist:
            list_item = '''
OneLineListItem:
    text: "User ''' + str(u.get_identifier()) + '''"
    on_release: User_''' + str(u.get_identifier()) + '''.trigger_action()
    MDCheckbox:
        id: User_''' + str(u.get_identifier()) + '''
        size_hint: None, None
        size: dp(31), dp(31)
        name: "''' + str(u.get_identifier()) + '''"
        center_y: self.parent.center_y
        center_x: self.parent.width - dp(35)
        active: False
        group: "users"
        callback: app.plot_map(self.name, self.active)
'''
            self.user_list.add_widget(Builder.load_string(list_item))

        animation = Animation(center_y=-35, duration=0.25)
        animation.start(self.card)
        self.can_press = True

    def start_clustering(self):
        if self.can_press is True:
            if self.dataset_file is not None:
                self.can_press = False
                threading.Thread(target=self.worker).start()
            else:
                self.file_error.text = "Load a dataset first"
                self.file_label.text_color = get_color_from_hex("D50000")
        else:
            self.error_message("Clustering already going on")

    def choose_file(self):
        root = tk.Tk()
        root.withdraw()
        self.dataset_file = filedialog.askopenfilename()
        file_name = os.path.basename(self.dataset_file)
        if file_name is not "":
            self.file_label.text = file_name
            self.file_error.text = ""
            self.file_label.text_color = self.theme_cls.primary_color

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

    def show_users_menu(self):
        if self.userlist is not None:
            if self.user_card_opened:
                animation = Animation(y=-self.users_card.height + 45, duration=0.25)
                animation.start(self.users_card)
                self.user_card_opened = False
                self.users_button.icon = "arrow-up"
            else:
                animation = Animation(y=- 45, duration=0.25)
                animation.start(self.users_card)
                self.user_card_opened = True
                self.users_button.icon = "arrow-down"
        else:
            self.error_message("Similarities not extracted")

    def plot_map(self, id, active):
        if active:
            print("User " + str(id))

    @staticmethod
    def error_message(message):
        Snackbar(text=message).show()

    def change_theme(self, active):
        if active:
            self.theme_cls.theme_style = 'Dark'
            self.map = plot_map('dark', self.osm)
            if self.map_view is not None and self.osm is False:
                self.map_view.reload()
        else:
            self.theme_cls.theme_style = 'Light'
            self.map = plot_map('light', self.osm)
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
        self.file_label = main_widget.ids.dataset_file
        self.file_error = main_widget.ids.file_error
        self.card = main_widget.ids.card
        self.clust_progress = main_widget.ids.clust_progress
        self.clustering_label = main_widget.ids.clustering_label
        self.map_scr = main_widget.ids.map_scr
        self.users_button = main_widget.ids.users_button
        self.user_list = main_widget.ids.user_list
        self.users_card = main_widget.ids.users_card
        self.label_user = main_widget.ids.label_no_users
        self.layout_user = main_widget.ids.layout_user
        return main_widget

    def on_stop(self):
        os._exit(0)
