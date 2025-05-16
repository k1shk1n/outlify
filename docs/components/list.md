# List

The **List** module in **Outlify** helps structure list information, improving
readability and visual organization when displaying grouped data in
terminal applications. It is especially useful for presenting collections,
options, or summaries in a clean and consistent format.

To view the demo for the **List** module use:

```sh
python -m outlify.list
```

<div class="result" markdown>

```
Outlify helps you create list output in a beautiful format

The first one is the simplest: a titled list
Packages (4): ruff@1.0.0  pytest@1.2.3  mkdocs@3.2.1  mike@0.0.1

Continued...
```

</div>

---

## TitledList
If you need a simple titled list output, you can use `TitledList`.

```python
from outlify.list import TitledList

packages = ['first', 'second', 'third']
print(TitledList(packages))
```

<div class="result" markdown>

```
Content (3): first  second  third
```

</div>

### `title`
Customize the title prefix of the list. The count will be automatically appended.

```python
from outlify.list import TitledList

packages = ['first-package-1.0.0', 'second-package-1.2.3']
print(TitledList(packages, title='Packages'))
```

<div class="result" markdown>

```
Packages (2): first-package-1.0.0  second-package-1.2.3
```

</div>

### `separator`
Change how items are separated in the output. Default is two spaces.

```python
from outlify.list import TitledList

fruits = ['apple', 'banana', 'orange']
print(TitledList(fruits, separator=', '))
```

<div class="result" markdown>

```
Content (3): apple, banana, orange
```

</div>