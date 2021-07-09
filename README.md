# IMT-342

## Commands

### Basics

| Command    | Action                                                                                                                | Example usage and subcommand examples                                                        |
|------------|-----------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| roscore    | This starts the Master                                                                                                | $ roscore                                                                                    |
| rosrun     | This runs an executable program and creates nodes                                                                     | $ rosrun [package name] [executable name]                                                    |
| rosnode    | This shows information about nodes and lists the active nodes                                                         | $ rosnode info [node name] $ rosnode [subcommand] Subcommand: list                           |
| rostopic   | This shows information about ROS topics                                                                               | $ rostopic [subcommand] [topic name] Subcommands: echo, info, and type                       |
| rosmsg     | This shows information about the message types                                                                        | $ rosmsg [subcommand] [package name]/ [message type] Subcommands: show, type, and list       |
| rosservice | This displays the runtime information about various services and allows the display of messages being sent to a topic | $ rosservice [subcommand] [service name] Subcommands: args, call, find, info, list, and type |
| rosparam   | This is used to get and set parameters (data) used by nodes                                                           | $ rosparam [subcommand] [parameter] Subcommands: get, set, list, and delete                  |

### rosnode

~~~bash
rosnode info    #print information about node
rosnode kill    #kill a running node
rosnode list    #list active nodes
rosnode machine #list nodes running on a particular machine
rosnode ping    #test connectivity to node
~~~

### rostopic

~~~bash
rostopic bw     #display bandwidth used by topic
rostopic echo   #print messages to screen
rostopic find   #find topics by type
rostopic hz     #display publishing rate of topic    
rostopic info   #print information about active topic
rostopic list   #print information about active topics
rostopic pub    #publish data to topic
rostopic type   #print topic type
~~~

### Running

~~~bash
roslaunch package_name launch_file_name.launch  # Run program from launch file
rosrun package_name python_file_name.py         # Run program from python file
~~~

## Lessons

### Lesson 1

[![Video 1](https://img.youtube.com/vi/pfBdAWQ_I2U/hqdefault.jpg)](https://www.youtube.com/watch?v=pfBdAWQ_I2U)

### Lesson 2

[![Video 2](https://img.youtube.com/vi/pZK5M_7h0sY/hqdefault.jpg)](https://www.youtube.com/watch?v=pZK5M_7h0sY)
