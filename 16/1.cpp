#include <iostream>
#include <string>
#include <bitset>

int main() {
  const int len = 20;
  std::bitset<len> bit_array(1 << (len - 1));
  std::cout << bit_array << std::endl;

  int next_pos = 1;

  while(next_pos < len) {
    int last_pos_of_duplication = (3 * next_pos) - 1;
    for(int i = last_pos_of_duplication; i >= next_pos; i--) {
      if(i < len) {
        std::cout << len - i << std::endl;
        std::cout << len - (i-1)/2 << std::endl;
        std::cout << bit_array[len - i] << std::endl;
        std::cout << bit_array[len - (i-1)/2] << std::endl;
        std::cout << "\n" << std::endl;
        bit_array[len - (i - 1) / 2] = !bit_array[len - i];
      }
    }
    std::cout << bit_array << std::endl;
    next_pos = last_pos_of_duplication;
  }
}
