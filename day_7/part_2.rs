use std::fs;

fn is_valid(numbers: &[usize], result: usize, target: usize) -> bool {
    if numbers.is_empty() {
        return result == target;
    }

    let current_number = numbers[0];

    let result_add = result + current_number;
    let result_mult: usize;

    if current_number == 0 {
        result_mult = current_number;
    } else {
        result_mult = result * current_number;
    }

    let result_concat: usize = format!("{result}{current_number}").parse().unwrap();

    is_valid(&numbers[1..], result_add, target) ||
    is_valid(&numbers[1..], result_mult, target) ||
    is_valid(&numbers[1..], result_concat, target)
}

fn main() {
    let file = fs::read_to_string("input.txt").unwrap();
    let data = file.trim();
    
    let mut total = 0;

    for entry in data.split("\n") {
        let (result, numbers) = entry.split_once(": ").unwrap();

        let result_int: usize = result.parse().unwrap();
        let numbers_int: Vec<usize> = numbers.split(" ").map(|a| a.parse().unwrap()).collect();

        if is_valid(&numbers_int[..], 0, result_int) {
            total += result_int;
        }
    }

    println!("{total}");
}
