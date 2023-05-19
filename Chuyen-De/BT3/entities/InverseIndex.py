class InverseIndex:
  # This is constructor
  def __init__(self, freq, s):
    self.freq = freq
    self.s = s
  
  def __str__(self) -> str:
    return f'{self.freq=} {self.s=}'