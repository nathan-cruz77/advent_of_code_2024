use std::io;
use std::convert::TryInto;

fn is_valid(vec: &Vec<usize>) -> bool {
    let first = vec[0];
    let second = vec[1];

    if first == second {
        return false;
    }

    let increasing = first < second;

    for (index, index2) in (0..vec.len() - 1).zip(1..vec.len()) {
        let a: i64 = vec[index].try_into().unwrap();
        let b: i64 = vec[index2].try_into().unwrap();
        
        let diff = (a - b).abs();

        if diff < 1 || diff > 3 {
            return false;
        }

        if vec[index] > vec[index2] && increasing {
            return false;
        }

        if vec[index] < vec[index2] && !increasing {
            return false;
        }
    }

    true
}

fn main() -> Result<(), io::Error> {
    let mut vec1 = Vec::new();

    let mut total = 0;

    for line in io::stdin().lines() {
        let my_line = line?;
        let values = my_line.split(" ");

        for value in values {
            let value_int: usize = value.parse().unwrap();
            vec1.push(value_int);
        }

        if is_valid(&vec1) {
            total += 1;
        }

        vec1.clear()
    }

    println!("{total}");

    Ok(())
}
