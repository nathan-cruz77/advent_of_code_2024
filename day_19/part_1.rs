use std::fs;

fn backtrack(pattern: &str, towels: &Vec<&str>) -> bool {
    if pattern == "" {
        return true
    }

    for towel in towels {
        if pattern.starts_with(towel) && backtrack(pattern.strip_prefix(towel).unwrap(), towels) {
            return true
        }
    }

    false
}

fn main() {
    let file = fs::read_to_string("input.txt").unwrap();
    let data = file.trim();

    let (towels_data, patterns_data) = data.split_once("\n\n").unwrap();

    let towels: Vec<&str> = towels_data.split(", ").collect();
    let patterns: Vec<&str> = patterns_data.split("\n").collect();

    let mut solvable_patterns_count = 0;

    for pattern in patterns {
        if backtrack(pattern, &towels) {
            solvable_patterns_count += 1;
        }
    }

    println!("{solvable_patterns_count}");
}
