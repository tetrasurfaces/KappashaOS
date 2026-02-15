// Copyright (C) 2025 BlockChan Contributors
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.

use std::collections::VecDeque;

pub struct Martingale {
    pub size: f64,
    fib: f64,  // 0.618 for Fib retrace
    nodes: VecDeque<f64>,  // For history in curl detection
}

impl Martingale {
    pub fn new() -> Self {
        Martingale {
            size: 1.0,  // Starting size
            fib: 0.618,
            nodes: VecDeque::new(),
        }
    }

    pub fn hedge_double(&mut self, delta: f64) {
        if delta < -self.fib {  // Double on down (negative delta for left-spiral)
            self.size *= 2.0;
            println!("Hedged double: new size {}", self.size);
        }
    }

    pub fn curl_detect(&mut self, new_price: f64, rod_tension: f64) -> bool {
        // Update nodes with new price (moving nodes)
        if self.nodes.len() > 16 {  // Cap history
            self.nodes.pop_front();
        }
        self.nodes.push_back(new_price);
        // Sim curl detection: check if delta < -fib (left-handed downward retrace)
        if self.nodes.len() >= 2 {
            let delta = self.nodes.back().unwrap() - self.nodes.front().unwrap();
            if delta < -self.fib {
                println!("Anti-clockwise curl detected (rod tension: {})", rod_tension);
                return true;
            }
        }
        false
    }

    pub fn tangent_burn(&self) -> bool {
        // Stub for tangent detection: sim true for left-spiral burn
        // In real, use VecDeque history to check tangent (e.g., alignment > fib threshold)
        true  // Always burn on tangent for sim
    }

    pub fn burn_lamports(&self, amount: u64) {
        // Sim burn lamports (print for stub; real: emit event or token burn)
        println!("Burned {} lamports on tangent", amount);
    }
}

// For standalone testing (cargo test or run)
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hedge_double() {
        let mut martingale = Martingale::new();
        martingale.hedge_double(-0.7);  // Trigger double
        assert_eq!(martingale.size, 2.0);
        martingale.hedge_double(0.5);  // No trigger (positive)
        assert_eq!(martingale.size, 2.0);
    }

    #[test]
    fn test_curl_detect() {
        let mut martingale = Martingale::new();
        martingale.curl_detect(1.0, 0.5);  // Add node
        assert!(martingale.curl_detect(0.2, 0.5));  // Delta = -0.8 < -0.618 → true
    }

    #[test]
    fn test_tangent_burn() {
        let martingale = Martingale::new();
        assert!(martingale.tangent_burn());
        martingale.burn_lamports(1);
    }
}
