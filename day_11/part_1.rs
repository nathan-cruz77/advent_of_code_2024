use std::fs;
use std::collections::HashMap;


fn blink(stone: usize, n: usize, cache: &mut HashMap<(usize, usize), usize>) -> usize {
    if cache.contains_key(&(stone, n)) {
        return cache[&(stone, n)];
    }

    if n == 0 {
        cache.insert((stone, n), 1);
        return cache[&(stone, n)];
    }

    if stone == 0 {
        let result = blink(1, n - 1, cache);
        cache.insert((stone, n), result);

        return cache[&(stone, n)];
    }

    let stone_str = format!("{stone:?}");

    if stone_str.len() % 2 == 0 {
        let middle_index = stone_str.len() / 2;
        let (a, b) = stone_str.split_at(middle_index);

        let a_num: usize = a.parse().unwrap();
        let b_num: usize = b.parse().unwrap();

        let result = blink(a_num, n - 1, cache) + blink(b_num, n - 1, cache);
        cache.insert((stone, n), result);
    } else {
        let result = blink(stone * 2024, n - 1, cache);
        cache.insert((stone, n), result);
    }

    cache[&(stone, n)]
}

fn main() {
    let file = fs::read_to_string("input.txt").unwrap();
    let data = file.trim();

    let stones: Vec<usize> = data.split(" ").map(|stone| stone.parse().unwrap()).collect();

    let mut total: usize = 0;
    let mut cache: HashMap<(usize, usize), usize> = HashMap::new();

    for stone in stones {
        total += blink(stone, 25, &mut cache);
    }

    println!("{total}");
}
