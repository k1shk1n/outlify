# Decorators

The **Decorators** module in **Outlify** provides a collection of decorators
designed to extend the capabilities of features, preserving the original
feature signatures and metadata and adding useful behavior.

To view the demo for the **Decorators** module use:

```sh
python -m outlify.decorators
```

<div class="result" markdown>

```
    @timer()
    def dummy_func(a: int, b: int) -> int:
        return a + b
    
Function 'dummy_func' took 00:00:00.123

Continued...
```

</div>

---

## timer