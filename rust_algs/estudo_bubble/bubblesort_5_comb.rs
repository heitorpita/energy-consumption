use std::io::{self, Read};

const SHRINK: f64 = 1.3;

fn bubble_sort(v: &mut [i32]) {
    let mut gap = v.len();
    let mut trocou = true;

    while gap > 1 || trocou {
        gap = ((gap as f64) / SHRINK) as usize;
        if gap < 1 {
            gap = 1;
        }

        trocou = false;
        for j in 0..v.len() - gap {
            if v[j] > v[j + gap] {
                v.swap(j, j + gap);
                trocou = true;
            }
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
