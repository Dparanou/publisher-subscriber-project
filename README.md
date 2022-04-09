# Publisher Subscriber Architecture

Implementation of a simple version of a Publish-Subscribe (Pub/Sub) system using Python3

### The required packages to run the application are:

- socket
- argparse
- threading
- sys
- time

The application containes 3 main entities:

1. The Broker (_broker.py_) which connects the Publishers and the Subscribers together
2. The Subscriber (_subscriber.py_) which connects to the Broker, subscribe/unsubscribe to one or more topics and receives notifications about the topics that he/she is subscribed
3. The Publisher (_publisher.py_) which connects to the Broker and publishes messages to topics

To properly run the application you should run the following commands.

First, the Broker must be start:

```sh
python3 broker.py -s 9001 -p 9000
```

> The arguments indicate the ports where they will connect:
>
> - the subscriber port (-s)
> - the publisher port (-p)

Then, the Subscriber can connect to the Broker by executing

```sh
python3 subscriber.py -i s1 -r 8000 -h localhost -p 9001 -f subscriber1.txt
```

> The arguments indicate :
>
> - the subscriber ID (-i)
> - the subscriber port (-r)
> - the Broker IP address (-h)
> - the Broker port (-p)
> - an optional parameter that indicates a file name where there are commands that the subscriber will execute once started and connected to the broker, before giving control to the user from the keyboard (-f)

Finally, the Publisher can connect to the Broker by executing

```sh
python3 publisher.py -i p1 -r 9000 -h localhost -p 9000 -f publisher1.txt
```

> The arguments indicate :
>
> - the publisher. ID (-i)
> - the publisher. port (-r)
> - the Broker IP address (-h)
> - the Broker port (-p)
> - an optional parameter that indicates a file name where there are commands that the publisher will execute once started and connected to the broker, before giving control to the user from the keyboard (-f)

After connection of a Publisher and a Subscriber, they both can run commands and publish or subscribe/unsubscribe respectively.

Example of command for Publisher:

```sh
p1 pub #hello This is the first message
```

Example of command for Subscriber:

```sh
s1 sub #hello
```

Finally, when a Publisher publish something in a topic, the Subscriber that is subscribed to this topic, will recieve a notification.
