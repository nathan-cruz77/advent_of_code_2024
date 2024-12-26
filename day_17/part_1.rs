use std::collections::HashMap;
use std::fs;


fn combo(memory: &HashMap<&str, usize>, operand: usize) -> usize {
    match operand {
        4 => memory["A"],
        5 => memory["B"],
        6 => memory["C"],
        other => other,
    }
}


fn adv(memory: &mut HashMap<&str, usize>, operand: usize) {
    let new_value = memory["A"] >> combo(memory, operand);
    memory.insert("A", new_value);
}


fn bxl(memory: &mut HashMap<&str, usize>, operand: usize) {
    let new_value = memory["B"] ^ operand;
    memory.insert("B", new_value);
}


fn bst(memory: &mut HashMap<&str, usize>, operand: usize) {
    let new_value = combo(memory, operand) % 8;
    memory.insert("B", new_value);
}


fn bxc(memory: &mut HashMap<&str, usize>, _operand: usize) {
    let new_value = memory["B"] ^ memory["C"];
    memory.insert("B", new_value);
}


fn out(memory: &HashMap<&str, usize>, operand: usize) -> usize {
    combo(memory, operand) % 8
}


fn bdv(memory: &mut HashMap<&str, usize>, operand: usize) {
    let new_value = memory["A"] >> combo(memory, operand);
    memory.insert("B", new_value);
}


fn cdv(memory: &mut HashMap<&str, usize>, operand: usize) {
    let new_value = memory["A"] >> combo(memory, operand);
    memory.insert("C", new_value);
}

fn run(memory: &mut HashMap<&str, usize>, program: &Vec<usize>, out_vec: &mut Vec<usize>) {
    let mut exec_pointer = 0;

    while exec_pointer < program.len() - 1 {
        let opcode = program[exec_pointer];
        let operand = program[exec_pointer + 1];

        match opcode {
            0 => adv(memory, operand),
            1 => bxl(memory, operand),
            2 => bst(memory, operand),
            3 => {
                if memory["A"] != 0 {
                    exec_pointer = operand;
                } else {
                    exec_pointer += 2;
                }
            },
            4 => bxc(memory, operand),
            5 => {
                let output = out(&memory, operand);
                out_vec.push(output);
            },
            6 => bdv(memory, operand),
            7 => cdv(memory, operand),
            _ => {}
        }

        if opcode != 3 {
            exec_pointer += 2;
        }

    }
}


fn main() {
    let mut memory = HashMap::new();
    let mut program = Vec::new();
    let mut out_vec = Vec::new();

    let file = fs::read_to_string("input.txt").unwrap();
    let data = file.trim();

    let (memory_data, program_data) = data.split_once("\n\n").unwrap();

    for mut memory_entry in memory_data.split("\n") {
        memory_entry = memory_entry.strip_prefix("Register ").unwrap();

        let (key, value) = memory_entry.split_once(": ").unwrap();
        let value_num: usize = value.parse().unwrap();

        memory.insert(key, value_num);
    }

    for program_entry in program_data.strip_prefix("Program: ").unwrap().split(",") {
        let program_entry_num: usize = program_entry.parse().unwrap();
        program.push(program_entry_num);
    }

    run(&mut memory, &program, &mut out_vec);

    println!("{out_vec:?}");
}
