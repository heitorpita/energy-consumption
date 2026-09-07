use std::io::{self, Read};

fn bubble_sort(v: &mut [i32]) {
    let mut inicio = 0usize;
    let mut fim = v.len().saturating_sub(1);

    while inicio < fim {
        let mut trocou = false;

        for j in inicio..fim {
            if v[j] > v[j + 1] {
                v.swap(j, j + 1);
                trocou = true;
            }
        }
        fim -= 1;

        for j in (inicio..fim).rev() {
            if v[j] > v[j + 1] {
                v.swap(j, j + 1);
                trocou = true;
            }
        }
        inicio += 1;

        if !trocou {
            break;
        }
    }
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut it = input.split_whitespace();

    let n: usize = it.next().unwrap().parse().unwrap();
    let mut v: Vec<i32> = (0..n).map(|_| it.next().unwrap().parse().unwrap()).collect();

    bubble_sort(&mut v);

    println!("{n}");
    let strs: Vec<String> = v.iter().map(|x| x.to_string()).collect();
    println!("{}", strs.join(" "));
}
