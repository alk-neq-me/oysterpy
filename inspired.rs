fn main() {
    let d = Err::<_, i32>(2).map(|_: &str| "hello");
    println!("{:?}", d);
}
