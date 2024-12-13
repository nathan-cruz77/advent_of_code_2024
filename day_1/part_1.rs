use std::io;

fn main() -> Result<(), io::Error> {
    let mut vec1 = Vec::new();
    let mut vec2 = Vec::new();

    for line in io::stdin().lines() {
        let my_line = line?;
        let (a, b) = my_line.split_once("   ").unwrap();

        let a_int = a.parse::<i32>().unwrap();
        vec1.push(a_int);
        
        let b_int = b.parse::<i32>().unwrap();
        vec2.push(b_int);
    }

    vec1.sort();
    vec2.sort();

    let mut total = 0;

    for (a, b) in vec1.iter().zip(vec2.iter()) {
        total += i32::abs(a - b);
    }

    println!("{total}");

    Ok(())
}
