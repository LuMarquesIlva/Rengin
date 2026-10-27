# Rengin 0.0.1
### **Python Game Engine**
---
A python game engine that focus on being easy to use

## To Build the Editor:

# Dependencies:
- ninja-build
- pkg-config
- libusb-1.0
- libudev
- dbus-1
- libpipewire-0.3
- wayland-client **libwayland-dev on ubuntu**
- xkbcommon
- freetype2 **libfreetype-dev on ubuntu**
- x11 **libx11-dev on ubuntu**
- xrandr
- xinerama
- xcursor
- xi
- expat
- libxml-2.0 **libxml2-dev on ubuntu**
- dot **graphviz on ubuntu**
- doxygen
- xsltproc
- xmlto
- mdbook
- libegl-dev


**You need first to create a 'subprojects' folder on the root directory** if you do not have it, then;
```bash
    meson wrap install sdl3
    meson wrap install sdl3_ttf
    meson wrap install sdl3_image
    meson wrap install glfw
    meson wrap install imgui
    meson wrap install vulkan-headers # if using vulkan

    uv run BUILD_EDITOR.py
```

## **Features**

- [x] Have Moving Squares?
- [ ] Are You Able to Create a Game?
