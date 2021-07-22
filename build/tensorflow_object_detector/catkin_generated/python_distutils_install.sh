#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/rodri/Documents/imt342_IN_ws/src/tensorflow_object_detector"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/rodri/Documents/imt342_IN_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/rodri/Documents/imt342_IN_ws/install/lib/python2.7/dist-packages:/home/rodri/Documents/imt342_IN_ws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/rodri/Documents/imt342_IN_ws/build" \
    "/usr/bin/python2" \
    "/home/rodri/Documents/imt342_IN_ws/src/tensorflow_object_detector/setup.py" \
     \
    build --build-base "/home/rodri/Documents/imt342_IN_ws/build/tensorflow_object_detector" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/rodri/Documents/imt342_IN_ws/install" --install-scripts="/home/rodri/Documents/imt342_IN_ws/install/bin"
