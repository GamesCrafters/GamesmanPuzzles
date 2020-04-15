# Position Introduction

```
GET puzzles/<puzzle_id>/<variant_id>/<position_id>
```
When users are accessing the Web API, they need a way to input a puzzle position and return a result. We can do this by **serializing** the puzzle into a string code, which can be **deserialized** back into a puzzle. This part of the guide will show the methods needed 