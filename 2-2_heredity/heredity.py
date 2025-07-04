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

def gene_pass_proba(parent_gene_count):
    if parent_gene_count == 2:
        return 1 - PROBS["mutation"]
    elif parent_gene_count == 1:
        return 0.5
    else:
        return PROBS["mutation"]

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
    joint_proba = 1
    for person in people:
        num_genes = 0
        # If that person do not have parents in the same list
        if people[person]["mother"] not in people and people[person]["father"] not in people:
            if person in one_gene:
                num_genes = 1
            if person in two_genes:
                num_genes = 2
            joint_proba *= PROBS["gene"][num_genes]
            prob_trait = PROBS["trait"][num_genes][True]
            if person in have_trait:
                joint_proba *= prob_trait
            else:
                joint_proba *= (1 - prob_trait)

        # If that person have parents in the same list
        else:
            father_num_genes = 0
            mother_num_genes = 0
            if people[person]["father"] in two_genes:
                father_num_genes = 2
            if people[person]["mother"] in two_genes:
                mother_num_genes = 2
            if people[person]["father"] in one_gene:
                father_num_genes = 1
            if people[person]["mother"] in one_gene:
                mother_num_genes = 1

            mother_prob = gene_pass_proba(mother_num_genes)
            father_prob = gene_pass_proba(father_num_genes)

            if person in two_genes:
                joint_proba *= mother_prob * father_prob
                num_genes = 2
            elif person in one_gene:
                joint_proba *= mother_prob * (1-father_prob) + father_prob * (1-mother_prob)
                num_genes = 1
            else:
                joint_proba *= (1 - mother_prob) * (1 - father_prob)
                num_genes = 0

            prob_trait = PROBS["trait"][num_genes][True]
            if person in have_trait:
                joint_proba *= prob_trait
            else:
                joint_proba *= (1 - prob_trait)
    return joint_proba

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

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
        total_gene = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
        probabilities[person]["gene"][0] /= total_gene
        probabilities[person]["gene"][1] /= total_gene
        probabilities[person]["gene"][2] /= total_gene

        total_trait = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        probabilities[person]["trait"][True] /= total_trait
        probabilities[person]["trait"][False] /= total_trait

if __name__ == "__main__":
    main()
