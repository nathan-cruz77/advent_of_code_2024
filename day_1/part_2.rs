use std::io;

fn frequencies(vec: &Vec<usize>, item: usize) -> usize {
    let mut occurrences = 0;

    for i in vec {
        if *i == item {
            occurrences += 1
        }
    }

    occurrences
}

fn main() -> Result<(), io::Error> {
    let mut vec1 = Vec::new();
    let mut vec2 = Vec::new();

    for line in io::stdin().lines() {
        let my_line = line?;
        let (a, b) = my_line.split_once("   ").unwrap();

        let a_int = a.parse::<usize>().unwrap();
        vec1.push(a_int);
        
        let b_int = b.parse::<usize>().unwrap();
        vec2.push(b_int);
    }

    vec1.sort();
    vec2.sort();

    let mut total = 0;

    for a in vec1 {
        total += a * frequencies(&vec2, a);
    }

    println!("{total}");

    Ok(())
}
