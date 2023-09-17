fn main() {
    let d = Err::<_, i32>(2).map(|_: &str| "hello");
    println!("{:?}", d);

    let x: Result<&str, &str> = Err("erro");
    println!("{x:?}");
}
