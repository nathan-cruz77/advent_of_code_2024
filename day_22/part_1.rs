use std::fs;

fn nth_secret_number(seed: usize, nth: usize) -> usize {
    let prune_number = 16_777_216;
    let mut num = seed;

    for _ in 0..nth {
        num = ((num << 6) ^ num) % prune_number;
        num = ((num >> 5) ^ num) % prune_number;
        num = ((num << 11) ^ num) % prune_number;
    }

    num
}

fn main() {
    let file = fs::read_to_string("input.txt").unwrap();
    let data = file.trim();

    let secret_numbers: Vec<usize> = data.lines().map(|num| num.parse().unwrap()).collect();

    let mut total: usize = 0;

    for secret_number in secret_numbers {
        total += nth_secret_number(secret_number, 2_000);
    }

    println!("{total}");
}
