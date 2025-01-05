use std::fs;
use std::collections::HashMap;

fn backtrack<'a>(pattern: &'a str, towels: &Vec<&str>, cache: &mut HashMap<&'a str, usize>) -> usize {
    if pattern == "" {
        return 1
    }

    if cache.contains_key(pattern) {
        return cache[pattern]
    }

    let mut count: usize = 0;

    for towel in towels {
        if pattern.starts_with(towel) {
            count += backtrack(pattern.strip_prefix(towel).unwrap(), towels, cache);
        }
    }

    cache.insert(pattern, count);
    count
}

fn main() {
    let file = fs::read_to_string("input.txt").unwrap();
    let data = file.trim();

    let (towels_data, patterns_data) = data.split_once("\n\n").unwrap();

    let towels: Vec<&str> = towels_data.split(", ").collect();
    let patterns: Vec<&str> = patterns_data.split("\n").collect();

    let mut solutions_count = 0;
    let mut cache: HashMap<&str, usize> = HashMap::new();

    for pattern in patterns {
        solutions_count += backtrack(pattern, &towels, &mut cache);
    }

    println!("{solutions_count}");
}
