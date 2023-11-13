# Oyster 🏖️🦪

![Python Version](https://img.shields.io/badge/Python-%3E%3D%203.10.6-blue)
![Oysterpy Version](https://img.shields.io/badge/Oysterpy-1.0.0-brightgreen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/alk-neq-me/fortipass/blob/main/LICENSE)


A Python library providing Result and Option types inspired by the Rust programming language.

## Installation

You can install Oyster from source:

```
git clone https://github.com/alk-neq-me/oysterpy.git
cd oysterpy
python setup.py sdist bdist_wheel
pip install -e .
```

## Overview

Oyster is a library that brings the Result and Option types from Rust to Python. These types are designed to handle success and failure scenarios in a more expressive and type-safe way.

### Result

The Result type represents the result of an operation that can either succeed (`Ok`) or fail (`Err`). It allows you to handle errors explicitly and provides a more structured approach to error handling.

Example usage:

```python
from oysterpy.oyster import Result, Ok, Err

def divide(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Err("Cannot divide by zero")
    return Ok(a // b)

result = divide(10, 2)
if result.is_ok():
    print("Result:", result.unwrap())
else:
    print("Error:", result.unwrap_err())
```

#### as_result - decorator

```python
from oysterpy.oyster import as_result

@as_result
def unsafe_error() -> int:
    if True:
        raise Exception("Thrown Error")
    return 12

unsafe_error()  # // Err(_type='err', value='Thrown Error')

safed_error: Result[int, str] = unsafe_error()

if safed_error.is_ok():
    print(safe_error().unwrap())
```

### Option

The Option type represents an optional value that can be either `Some(value)` or `None`. It provides a safer alternative to handling nullable values by explicitly distinguishing between the presence and absence of a value.

Example usage:

```python
from oysterpy.oyster import Option, Some, None_

def get_user_name(user_id: int) -> Option[str]:
    if user_id in user_database:
        return Some(user_database[user_id].name)
    else:
        return None_()

user_id = 123
user_name = get_user_name(user_id)
if user_name.is_some():
    print("User name:", user_name.unwrap())
else:
    print("User not found")
```

### Pattern Matching

Oyster supports pattern matching, similar to Rust's `match` statement, to handle different cases of `Result` and `Option` values. Here's an example of pattern matching with `Result`:

```python
from oysterpy.oyster import Result, Ok, Err

def process_result(result: Result[int, str]):
    match result:
        case Ok(value):
            print("Success:", value)
        case Err(error):
            print("Error:", error)

process_result(Ok(42))  # Output: Success: 42
process_result(Err("Oops!"))  # Output: Error: Oops!
```

And here's an example of pattern matching with `Option`:

```python
from oysterpy.oyster import Option, Some, None_

def process_option(option: Option[int]):
    match option:
        case Some(value):
            print("Value:", value)
        case None_():
            print("No value")

process_option(Some(42))  # Output: Value: 42
process_option(None_())  # Output: No value
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/alk-neq-me/oysterpy).


## API Documentation

### Option

#### `OptionImpl` class

The `OptionImpl` class represents the `Option` type, which can either be `Some` (containing a value) or `None` (representing the absence of a value).

##### Methods

- `is_some() -> bool`: Returns `True` if the `Option` is `Some`, `False` otherwise.
- `is_none() -> bool`: Returns `True` if the `Option` is `None`, `False` otherwise.
- `is_some_and(f: Callable[[V], bool]) -> bool`: Returns the result of applying the given function `f` to the value if the `Option` is `Some`, or `False` if it is `None`.
- `and_(op: Option[F]) -> Option[F]`: Returns `op` if the `Option` is `Some`, or `None` otherwise.
- `and_then(op: Callable[[V], Option[F]]) -> Option[F]`: Applies the function `op` to the value if the `Option` is `Some` and returns the result, or returns `None` otherwise.
- `or_(op: Option[V]) -> Option[V]`: Returns `Some` with the value if the `Option` is `Some`, or `op` if it is `None`.
- `or_else(op: Callable[..., Option[V]]) -> Option[V]`: Returns `Some` with the value if the `Option` is `Some`, or the result of the function `op` if it is `None`.
- `map(f: Callable[[V], F]) -> Option[F]`: Applies the function `f` to the value if the `Option` is `Some` and returns the result as a new `Option`, or returns `None` otherwise.
- `map_or(default: F, f: Callable[[V], F]) -> F`: Applies the function `f` to the value if the `Option` is `Some` and returns the result, or returns `default` if it is `None`.
- `map_or_else(default: Callable[..., F], f: Callable[[V], F]) -> F`: Applies the function `f` to the value if the `Option` is `Some` and returns the result, or returns the result of the function `default` if it is `None`.
- `ok_or(err: B) -> Result[V, B]`: Returns `Ok` with the value if the `Option` is `Some`, or `Err` with `err` if it is `None`.
- `ok_or_else(err: Callable[..., B]) -> Result[V, B]`: Returns `Ok` with the value if the `Option` is `Some`, or `Err` with the result of the function `err` if it is `None`.
- `expect(msg: str) -> V`: Returns the value if the `Option` is `Some`, or raises an `ExpectException` with the given `msg` if it is `None`.
- `unwrap() -> V`: Returns the value if the `Option` is `Some`, or raises an `UnwrapException` if it is `None`.
- `unwrap_or(default: V) -> V`: Returns the value if the `Option` is `Some`, or returns `default` if it is `None`.
- `unwrap_or_self(f: Callable[..., V]) -> V`: Returns the value if the `Option` is `Some`, or returns the result of the function `f` if it is `None`.

#### `Some` class

The `Some` class represents the `Some` variant of the `Option` type, containing a value.

##### Methods

- `__str__() -> str`: Returns a string representation of the `Some` variant.

#### `None_` class

The `None_` class represents the `None` variant of the `Option` type, representing the absence of a value.

##### Methods

- `__str__() -> str`: Returns a string representation of the `None` variant.

#### `Option` type alias

The `Option` type alias represents the union of the `Some` and `None_` classes, representing an `Option` value.

---

### Result

#### `ResultImpl` class

The `ResultImpl` class represents the `Result` type, which can either be `Ok` (indicating a successful result) or `Err` (indicating an error result).

##### Methods

- `is_ok() -> bool`: Returns `True` if the `Result` is `Ok`, `False` otherwise.
- `is_ok_and(f: Callable[[T], bool]) -> bool`: Returns the result of applying the given function `f` to the value if the `Result` is `Ok`, or `False` if it is `Err`.
- `is_err() -> bool`: Returns `True` if the `Result` is `Err`, `False` otherwise.
- `is_err_and(f: Callable[[E], bool]) -> bool`: Returns the result of applying the given function `f` to the error if the `Result` is `Err`, or `False` if it is `Ok`.
- `ok() -> Option[T]`: Returns `Some` with the value if the `Result` is `Ok`, or `None` if it is `Err`.
- `err() -> Option[E]`: Returns `Some` with the error if the `Result` is `Err`, or `None` if it is `Ok`.
- `map(op: Callable[[T], U]) -> Result[U, E]`: Applies the function `op` to the value if the `Result` is `Ok` and returns the result as a new `Result`, or returns `Err` with the existing error if it is `Err`.
- `map_or(default: U, f: Callable[[T], U]) -> U`: Applies the function `f` to the value if the `Result` is `Ok` and returns the result, or returns `default` if it is `Err`.
- `map_or_else(default: Callable[[E], U], f: Callable[[T], U]) -> U`: Applies the function `f` to the value if the `Result` is `Ok` and returns the result, or returns the result of the function `default` applied to the error if it is `Err`.
- `map_err(op: Callable[[E], U]) -> Result[T, U]`: Applies the function `op` to the error if the `Result` is `Err` and returns the result as a new `Result`, or returns `Ok` with the existing value if it is `Ok`.
- `and_(res: Result[U, E]) -> Result[U, E]`: Returns `res` if the `Result` is `Ok`, or returns `Err` with the existing error if it is `Err`.
- `and_then(op: Callable[[T], Result[U, E]]) -> Result[U, E]`: Applies the function `op` to the value if the `Result` is `Ok` and returns the result, or returns `Err` with the existing error if it is `Err`.
- `or_(res: Result[T, U]) -> Result[T, U]`: Returns `

Ok` with the existing value if the `Result` is `Ok`, or returns `res` if it is `Err`.
- `or_else(op: Callable[[E], Result[T, U]]) -> Result[T, U]`: Returns `Ok` with the existing value if the `Result` is `Ok`, or returns the result of the function `op` applied to the error if it is `Err`.
- `expect(msg: str) -> T`: Returns the value if the `Result` is `Ok`, or raises an `UnwrapException` with the given `msg` if it is `Err`.
- `expect_err(msg: str) -> E`: Returns the error if the `Result` is `Err`, or raises an `UnwrapException` with the given `msg` if it is `Ok`.
- `unwrap() -> T`: Returns the value if the `Result` is `Ok`, or raises an `UnwrapException` if it is `Err`.
- `unwrap_or(default: T) -> T`: Returns the value if the `Result` is `Ok`, or returns `default` if it is `Err`.
- `unwrap_or_else(op: Callable[[E], T]) -> T`: Returns the value if the `Result` is `Ok`, or returns the result of the function `op` applied to the error if it is `Err`.
- `unwrap_err() -> E`: Returns the error if the `Result` is `Err`, or raises an `UnwrapException` if it is `Ok`.

#### `Ok` class

The `Ok` class represents the `Ok` variant of the `Result` type, indicating a successful result.

##### Methods

- `__str__() -> str`: Returns a string representation of the `Ok` variant.

#### `Err` class

The `Err` class represents the `Err` variant of the `Result` type, indicating an error result.

##### Methods

- `__str__() -> str`: Returns a string representation of the `Err` variant.

#### `Result` type alias

The `Result` type alias represents the union of the `Ok` and `Err` classes, representing a `Result` value.


------

Please note that you may need to update the `user_database` and other variables according to your specific implementation.


## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/alk-neq-me/oyster/blob/main/LICENSE) file for details.

---
