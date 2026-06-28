from dataclasses import dataclass

@dataclass(frozen=True)
class Gene:
    GeneID: str
    Chromosome: int
    Function: str