import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    result = dict()
    for cur_page, linked_pages in corpus.items():
        if page in cur_page:
            if len(linked_pages) == 0:
                for element in corpus:
                    result[element] = 1/len(corpus)
            else:
                for element in linked_pages:
                    result[element] = damping_factor / len(linked_pages)
    for key in corpus:
        if key not in result:
            result[key] = (1 - damping_factor)/len(corpus)
        else:
            result[key] += (1 - damping_factor)/len(corpus)
    print(result)
    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize a dictionary to count the number of visits (samples) per page
    result_dict = {key: 0 for key in corpus}

    # Randomly choose the first page to start the sampling process
    page = random.choice(list(corpus.keys()))
    result_dict[page] += 1  # Count this first visit

    # Get the transition model (probability distribution over next pages)
    # from the current page, according to damping factor
    list_keys = list(transition_model(corpus, page, damping_factor).keys())
    list_values = list(transition_model(corpus, page, damping_factor).values())

    # Sample the next page based on the probabilities
    next_sample = random.choices(list_keys, list_values)  # returns a list of one element

    # If more than one sample is needed, continue sampling
    if n > 1:
        for i in range(n - 1):
            # Record the visit to the sampled page
            result_dict[next_sample[0]] += 1

            # Get the next transition model from the current sampled page
            keys = list(transition_model(corpus, next_sample[0], damping_factor).keys())
            values = list(transition_model(corpus, next_sample[0], damping_factor).values())

            # Sample the next page based on this transition model
            next_sample = random.choices(keys, values)

    # Normalize the result_dict to get estimated PageRank (sum should be 1)
    for key in result_dict.keys():
        result_dict[key] /= n

    # Return the estimated PageRank values after n samples
    return result_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize PageRank values: start with equal probability for each page
    result_dict = {key: 1 / len(corpus) for key in corpus}

    # Dictionary to temporarily store updated PageRank values each iteration
    buffer_dict = {key: 0 for key in corpus}

    # Loop until values converge (change less than threshold ε for all pages)
    converged = False
    while not converged:
        converged = True  # Will remain True if no significant changes are found

        # Iterate through each page to compute its new PageRank
        for page_p, linked_pages in corpus.items():
            # Base PageRank from random jump factor (i.e., user teleports anywhere)
            new_pr = (1 - damping_factor) / len(corpus)

            # Loop over all other pages to see how they contribute to page_p
            for other_page, other_links in corpus.items():
                if not other_links:
                    # Treat pages with no outgoing links as linking to all pages
                    new_pr += damping_factor * (result_dict[other_page] / len(corpus))
                elif page_p in other_links:
                    # If other_page links to page_p, it contributes to its PageRank
                    new_pr += damping_factor * (result_dict[other_page] / len(other_links))

            # Store the updated PageRank value in the buffer
            buffer_dict[page_p] = new_pr

        # Check if all PageRank values have converged
        for key in buffer_dict:
            # If the change is above the threshold, another iteration is needed
            if abs(buffer_dict[key] - result_dict[key]) >= 0.001:
                converged = False

        # Update the result_dict with the newly computed values (always do this)
        result_dict = buffer_dict.copy()

    # Return the final PageRank values after convergence
    return result_dict


if __name__ == "__main__":
    main()
