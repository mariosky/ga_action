# Channel Map
This library takes [goless](http://goless.readthedocs.io/en/latest/) channels and makes them easier to manage and compose in an object oriented style. The design was inspired by the *metabolic pathways* which are series of linked chemical reactions occurring within a cell. A comparison can be made to the way data is processed using channels, data flows into different paths of execution which may or may not be active.

### How to use?
Create a MetroMap object. This object will be used as a factory to instantiate channels, stations and paths.
```python
map = MetroMap()
```
Then create the nodes of the graph, this means channels and stations.
```python
def duplicate(x):
    return x * x

map.channel('1')
map.station('duplicate', duplicate)
```
Now create a path for the data.
```python
path = map.path('duplicate_path')
path.begin('duplicate')
path.to('1')
```
Test the path.
```python
def send_data():
    path.send(1)

def recieve_data():
    print(path.recieve())

go(send_data)
recieve_data()
```

### TODO
* Unit tests.
* Fix bugs. Only works if you send the data first. Then recieve it.
* Fix pause.
* Add automatic start.
