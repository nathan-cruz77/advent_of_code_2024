use std::fs;

fn to_num(data: &str) -> f64 {
    let (_, num) =
        if data.contains("+") {
            data.split_once("+").unwrap()
        } else {
            data.split_once("=").unwrap()
        };

    num.parse().unwrap()
}


fn to_coords(data: &str) -> (f64, f64) {
    let (_, rest) = data.split_once(": ").unwrap();
    let (a, b) = rest.split_once(", ").unwrap();

    (to_num(a), to_num(b))
}


fn main() {
    let file = fs::read_to_string("input.txt").unwrap();
    let data = file.trim();

    let mut total_cost = 0.0;

    for machine in data.split("\n\n") {
        let split_data: Vec<&str> = machine.split("\n").collect();

        let button_a = split_data[0];
        let button_b = split_data[1];
        let claw = split_data[2];

        let (x_a, y_a) = to_coords(button_a);
        let (x_b, y_b) = to_coords(button_b);
        let (mut x_t, mut y_t) = to_coords(claw);

        x_t += 10_000_000_000_000.0;
        y_t += 10_000_000_000_000.0;

        let mut a: f64 = (y_t - (y_b * x_t / x_b)) / (y_a - (x_a * y_b / x_b));
        let mut b: f64 = (x_t - (x_a * a)) / x_b;

        a = a.round();
        b = b.round();

        if (a * x_a + b * x_b != x_t) || (a * y_a + b * y_b != y_t) {
            continue;
        }

        total_cost += a * 3.0;
        total_cost += b;
    }

    println!("{total_cost}")
}
