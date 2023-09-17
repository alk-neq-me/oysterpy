from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Generic, Literal, TypeAlias, TypeVar, Union

from oysterpy.exceptions import ExpectException, UnreachableException, UnwrapException

import functools


def unwrap_failed(msg: str, error) -> Exception:
    return UnwrapException(f"{msg}: {error!r}")


def expect_failed(msg: str) -> Exception:
    return ExpectException(msg)


# Option
V = TypeVar("V")
F = TypeVar("F")
B = TypeVar("B")

# Result
T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")


# -------------------- Option --------------------

@dataclass
class OptionImpl(Generic[V]):
    _type: Literal["some", "none"] = field(init=False)
    value: Union[V, None]
    def is_some(self):
        match self:
            case Some(_):
                return True
            case None_():
                return False
            case _:
                raise UnreachableException("Unreachable")

    def is_none(self):
        match self:
            case None_():
                return True
            case Some(_):
                return False
            case _:
                raise UnreachableException("Unreachable")

    def is_some_and(self, f: Callable[[V], bool]) -> bool:
        match self:
            case None_():
                return False
            case Some(x):
                return f(x)
            case _:
                raise UnreachableException("Unreachable")

    def and_(self, op: Option[F]) -> Option[F]:
        match self:
            case Some(_):
                return op
            case None_():
                return None_()
            case _:
                raise UnreachableException("Unreachable")

    def and_then(self, op: Callable[[V], Option[F]]) -> Option[F]:
        match self:
            case Some(x):
                return op(x)
            case None_():
                return None_()
            case _:
                raise UnreachableException("Unreachable")

    def or_(self, op: Option[V]) -> Option[V]:
        match self:
            case Some(t):
                return Some(t)
            case None_():
                return op
            case _:
                raise UnreachableException("Unreachable")

    def or_else(self, op: Callable[..., Option[V]]) -> Option[V]:
        match self:
            case Some(t):
                return Some(t)
            case None_():
                return op()
            case _:
                raise UnreachableException("Unreachable")

    def map(self, f: Callable[[V], F]) -> Option[F]:
        match self:
            case Some(x):
                return Some(f(x))
            case None_():
                return None_()
            case _:
                raise UnreachableException("Unreachable")

    def map_or(self, default: F, f: Callable[[V], F]) -> F:
        match self:
            case Some(x):
                return f(x)
            case None_():
                return default
            case _:
                raise UnreachableException("Unreachable")

    def map_or_else(self, default: Callable[..., F], f: Callable[[V], F]) -> F:
        match self:
            case Some(x):
                return f(x)
            case None_():
                return default()
            case _:
                raise UnreachableException("Unreachable")

    def ok_or(self, err: B) -> Result[V, B]:
        match self:
            case Some(v):
                return Ok(v)
            case None_():
                return Err(err)
            case _:
                raise UnreachableException("Unreachable")

    def ok_or_else(self, err: Callable[..., B]) -> Result[V, B]:
        match self:
            case Some(v):
                return Ok(v)
            case None_():
                return Err(err())
            case _:
                raise UnreachableException("Unreachable")

    def expect(self, msg: str) -> V:
        match self:
            case Some(v):
                return v
            case None_():
                raise expect_failed(msg)
            case _:
                raise UnreachableException("Unreachable")

    def unwrap(self) -> V:
        match self:
            case Some(v):
                return v
            case None_():
                raise UnwrapException("called `Option.unwrap()` on a `None` value")
            case _:
                raise UnreachableException("Unreachable")

    def unwrap_or(self, default: V) -> V:
        match self:
            case Some(v):
                return v
            case None_():
                return default
            case _:
                raise UnreachableException("Unreachable")

    def unwrap_or_self(self, f: Callable[..., V]) -> V:
        match self:
            case Some(v):
                return v
            case None_():
                return f()
            case _:
                raise UnreachableException("Unreachable")


@dataclass
class Some(OptionImpl[V]):
    _type = "some"
    value: V

    def __str__(self) -> str:
        return f"Some({self.value!r})"


@dataclass
class None_(OptionImpl[V]):
    _type = "none"
    value: None = field(default=None, init=False)

    def __str__(self) -> str:
        return "None"


Option: TypeAlias = Union[Some[V], None_[V]]

# -------------------- Result --------------------


@dataclass
class ResultImpl(Generic[T, E]):
    _type: Literal["ok", "err"] = field(init=False)
    value: Union[T, E]
    def is_ok(self) -> bool:
        match self:
            case Ok(_): 
                return True 
            case Err(_): 
                return False
            case _:
                raise UnreachableException("Unreachable")

    def is_ok_and(self, f: Callable[[T], bool]) -> bool:
        match self:
            case Err(_):
                return False
            case Ok(e):
                return f(e)
            case _:
                raise UnreachableException("Unreachable")

    def is_err(self) -> bool:
        return self._type == "err"

    def is_err_and(self, f: Callable[[E], bool]) -> bool:
        match self:
            case Ok(_):
                return False
            case Err(e):
                return f(e)
            case _:
                raise UnreachableException("Unreachable")

    def ok(self) -> Option[T]:
        match self:
            case Ok(x):
                return Some(x)
            case Err(_):
                return None_[T]()
            case _:
                raise UnreachableException("Unreachable")

    def err(self) -> Option[E]:
        match self:
            case Ok(_):
                return None_[E]()
            case Err(e):
                return Some(e)
            case _:
                raise UnreachableException("Unreachable")

    def map(self, op: Callable[[T], U]) -> Result[U, E]:
        match self:
            case Ok(t):
                return Ok(op(t))
            case Err(e):
                return Err(e)
            case _:
                raise UnreachableException("Unreachable")

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        match self:
            case Ok(t):
                return f(t)
            case Err(_):
                return default
            case _:
                raise UnreachableException("Unreachable")

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        match self:
            case Ok(t):
                return f(t)
            case Err(e):
                return default(e)
            case _:
                raise UnreachableException("Unreachable")

    def map_err(self, op: Callable[[E], U]) -> Result[T, U]:
        match self:
            case Ok(t):
                return Ok(t)
            case Err(e):
                return Err(op(e))
            case _:
                raise UnreachableException("Unreachable")

    def and_(self, res: Result[U, E]) -> Result[U, E]:
        match self:
            case Ok(_):
                return res
            case Err(e):
                return Err(e)
            case _:
                raise UnreachableException("Unreachable")

    def and_then(self, op: Callable[[T], Result[U, E]]) -> Result[U, E]:
        match self:
            case Ok(t):
                return op(t)
            case Err(e):
                return Err(e)
            case _:
                raise UnreachableException("Unreachable")

    def or_(self, res: Result[T, U]) -> Result[T, U]:
        match self:
            case Ok(v):
                return Ok(v)
            case Err(_):
                return res
            case _:
                raise UnreachableException("Unreachable")

    def or_else(self, op: Callable[[E], Result[T, U]]) -> Result[T, U]:
        match self:
            case Ok(t):
                return Ok(t)
            case Err(e):
                return op(e)
            case _:
                raise UnreachableException("Unreachable")

    def expect(self, msg: str) -> T:
        match self:
            case Ok(t):
                return t
            case Err(e):
                raise unwrap_failed(msg, e)
            case _:
                raise UnreachableException("Unreachable")

    def expect_err(self, msg: str) -> E:
        match self:
            case Ok(t):
                raise unwrap_failed(msg, t)
            case Err(e):
                return e
            case _:
                raise UnreachableException("Unreachable")

    def unwrap(self) -> T:
        match self:
            case Ok(t):
                return t
            case Err(e):
                raise unwrap_failed("called `Result.unwrap()` on an `Err` value", e)
            case _:
                raise UnreachableException("Unreachable")

    def unwrap_or(self, default: T) -> T:
        match self:
            case Ok(t):
                return t
            case Err(_):
                return default
            case _:
                raise UnreachableException("Unreachable")

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        match self:
            case Ok(t):
                return t
            case Err(e):
                return op(e)
            case _:
                raise UnreachableException("Unreachable")

    def unwrap_err(self) -> E:
        match self:
            case Ok(t):
                raise unwrap_failed("called `Result.unwrap_err()` on an `Ok` value", t)
            case Err(e):
                return e
            case _:
                raise UnreachableException("Unreachable")


@dataclass
class Ok(ResultImpl[T, E]):
    _type = "ok"
    value: T

    def __str__(self) -> str:
        return f"Ok({self.value!r})"


@dataclass
class Err(ResultImpl[T, E]):
    _type = "err"
    value: E

    def __str__(self) -> str:
        return f"Err({self.value!r})"


Result: TypeAlias = Union[Ok[T, E], Err[T, E]]


ReturnType = TypeVar("ReturnType")

def as_result(fn: Callable[..., ReturnType]) -> Callable[..., Result[ReturnType, str]]:
    @functools.wraps(fn)
    def wrapper(*args, **kwargs) -> Result[ReturnType, str]:
        try:
            func = fn(*args, **kwargs)
            return Ok(func)
        except StopIteration:
            return Err("StopIteration")
        except Exception as e:
            return Err(str(e))
    return wrapper

def as_option(fn: Callable[..., ReturnType]) -> Callable[..., Option[ReturnType]]:
    @functools.wraps(fn)
    def wrapper(*args, **kwargs) -> Option[ReturnType]:
        func = fn(*args, **kwargs)
        if func is None:
            return None_[ReturnType]()
        return Some[ReturnType](func)
    return wrapper
