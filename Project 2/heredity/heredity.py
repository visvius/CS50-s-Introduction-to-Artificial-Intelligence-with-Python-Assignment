import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}

""" people dict sample structure
people = {
    "Harry": {
        "name": "Harry",
        "mother": "Lily",
        "father": "James",
        "trait": None
    },
    "James": {
        "name": "James",
        "mother": None,
        "father": None,
        "trait": True
    },
    "Lily": {
        "name": "Lily",
        "mother": None,
        "father": None,
        "trait": False
    }
}
"""

def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

# helper fn for joint_probability 
# finds probabilty of inheritance of gene
def gene_pass_prob(gene_count):
    if gene_count == 2:
        return 1 - PROBS["mutation"]
    elif gene_count == 1:
        return 0.5
    else:
        return PROBS["mutation"]

# finds number of genes (for a parent usually)
def get_gene_count(name, one_gene, two_genes):
    if name in one_gene:
        return 1
    elif name in two_genes:
        return 2
    return 0

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # stores the final prob
    total_prob = 1

    for person in people:
        # FINDING RELATED DATA ABOUT PERSON
        inherit_prob = 1
        trait_prob = 1

        # FINDING INHERITANCE PROBABILITY

        mother = people[person]["mother"]
        father = people[person]["father"]
        # finding inherit_prob if parents are present in data
        if mother and father:
            # finding parents gene count
            mother_gene_count = get_gene_count(mother, one_gene, two_genes)
            father_gene_count = get_gene_count(father, one_gene, two_genes)
            # finding gene inheritance prob
            mother_inheritance = gene_pass_prob(mother_gene_count)
            father_inheritance = gene_pass_prob(father_gene_count)
            
            # condition for how many genes person has
            if person in one_gene:
                inherit_prob = ( mother_inheritance*(1-father_inheritance) ) + ( father_inheritance*(1-mother_inheritance) )
            elif person in two_genes:
                inherit_prob = mother_inheritance * father_inheritance
            else: 
                inherit_prob = (1-mother_inheritance) * (1-father_inheritance)

        # finding inherit prob if parent data not available
        else:
            if person in two_genes:
                inherit_prob = PROBS["gene"][2]
            elif person in one_gene:
                inherit_prob = PROBS["gene"][1]
            else:
                inherit_prob = PROBS["gene"][0]
        
        # inherit prob known at this point

        # FINDING TRAIT PROBABILITY
        person_gene_count = get_gene_count(person, one_gene, two_genes)
        if person in have_trait:
            trait_prob = PROBS["trait"][person_gene_count][True]
        else:
            trait_prob = PROBS["trait"][person_gene_count][False]
        
        # TOTAL PROB of PERSON having specified GENES and having/not having TRAITS
        person_prob = inherit_prob * trait_prob

        total_prob *= person_prob
    
    return total_prob
    


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:
        # updating the gene probabilitiy
        if person in two_genes:
            probabilities[person]["gene"][2] += p
        elif person in one_gene:
            probabilities[person]["gene"][1] += p
        else: 
            probabilities[person]["gene"][0] += p

        # updating the trait probability
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        for distribution in probabilities[person]: # gene and trait are distributions
            # finding total sum
            total = sum(probabilities[person][distribution].values())
            # normalizing
            for (key, value) in probabilities[person][distribution].items():
                probabilities[person][distribution][key] = value/total
                



if __name__ == "__main__":
    main()
