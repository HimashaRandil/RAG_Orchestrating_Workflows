import json
from utils.logger.logging import logger as logger


def generate_book_descriptions():
    """
    Generate 50 book descriptions with title, author, year, and description.
    You can replace this with AI-generated content or manually curated books.
    """

    books = [
        {
            "id": 1,
            "title": "The Midnight Library",
            "author": "Matt Haig",
            "year": 2020,
            "description": "A philosophical novel about a woman who finds herself in a magical library between life and death, exploring infinite possibilities of different lives she could have lived.",
        },
        {
            "id": 2,
            "title": "Atomic Habits",
            "author": "James Clear",
            "year": 2018,
            "description": "A comprehensive guide to building good habits and breaking bad ones, focusing on small changes that compound over time to create remarkable results.",
        },
        {
            "id": 3,
            "title": "The Seven Husbands of Evelyn Hugo",
            "author": "Taylor Jenkins Reid",
            "year": 2017,
            "description": "A captivating novel about a reclusive Hollywood icon who finally decides to tell her life story to an unknown journalist, revealing decades of secrets and scandals.",
        },
        {
            "id": 4,
            "title": "Educated",
            "author": "Tara Westover",
            "year": 2018,
            "description": "A powerful memoir about a woman who grows up in a survivalist family in rural Idaho and eventually earns a PhD from Cambridge University, exploring themes of education, family, and identity.",
        },
        {
            "id": 5,
            "title": "The Silent Patient",
            "author": "Alex Michaelides",
            "year": 2019,
            "description": "A psychological thriller about a woman who refuses to speak after allegedly murdering her husband, and the psychotherapist determined to understand her silence.",
        },
        {
            "id": 6,
            "title": "Sapiens",
            "author": "Yuval Noah Harari",
            "year": 2014,
            "description": "A thought-provoking exploration of human history, examining how Homo sapiens became the dominant species and shaped the modern world through cognitive, agricultural, and scientific revolutions.",
        },
        {
            "id": 7,
            "title": "The Alchemist",
            "author": "Paulo Coelho",
            "year": 1988,
            "description": "A philosophical novel about a young shepherd's journey to find treasure, learning about dreams, destiny, and the importance of listening to one's heart.",
        },
        {
            "id": 8,
            "title": "Dune",
            "author": "Frank Herbert",
            "year": 1965,
            "description": "A science fiction epic set on the desert planet Arrakis, following Paul Atreides as he navigates political intrigue, religious prophecy, and ecological themes in a complex interstellar society.",
        },
        {
            "id": 9,
            "title": "The Power of Now",
            "author": "Eckhart Tolle",
            "year": 1997,
            "description": "A spiritual guide to living in the present moment, offering practical teachings on mindfulness, consciousness, and finding peace through present-moment awareness.",
        },
        {
            "id": 10,
            "title": "1984",
            "author": "George Orwell",
            "year": 1949,
            "description": "A dystopian novel depicting a totalitarian society where Big Brother watches everything, exploring themes of surveillance, propaganda, and the manipulation of truth.",
        },
        {
            "id": 11,
            "title": "Where the Crawdads Sing",
            "author": "Delia Owens",
            "year": 2018,
            "description": "A coming-of-age mystery about a young girl who raises herself in the marshes of North Carolina, becoming a suspect in a murder case that rocks her small town.",
        },
        {
            "id": 12,
            "title": "The Handmaid's Tale",
            "author": "Margaret Atwood",
            "year": 1985,
            "description": "A dystopian novel set in a totalitarian society where women have lost their rights and are forced into reproductive servitude, exploring themes of power, control, and resistance.",
        },
        {
            "id": 13,
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "year": 1960,
            "description": "A classic American novel about racial injustice in the American South, told through the eyes of Scout Finch as her father defends a Black man falsely accused of rape.",
        },
        {
            "id": 14,
            "title": "The Kite Runner",
            "author": "Khaled Hosseini",
            "year": 2003,
            "description": "A powerful story of friendship, guilt, and redemption set against the backdrop of Afghanistan's tumultuous history, following Amir's journey to atone for childhood betrayals.",
        },
        {
            "id": 15,
            "title": "Harry Potter and the Philosopher's Stone",
            "author": "J.K. Rowling",
            "year": 1997,
            "description": "The first book in the beloved fantasy series about a young wizard who discovers his magical heritage and begins his education at Hogwarts School of Witchcraft and Wizardry.",
        },
        {
            "id": 16,
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "year": 1925,
            "description": "A classic American novel set in the Jazz Age, exploring themes of wealth, love, and the American Dream through the story of Jay Gatsby's obsession with Daisy Buchanan.",
        },
        {
            "id": 17,
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "year": 1813,
            "description": "A romantic novel about Elizabeth Bennet and Mr. Darcy, exploring themes of love, class, and social expectations in Regency England.",
        },
        {
            "id": 18,
            "title": "The Lord of the Rings: The Fellowship of the Ring",
            "author": "J.R.R. Tolkien",
            "year": 1954,
            "description": "The first volume of the epic fantasy trilogy, following hobbit Frodo Baggins as he begins his quest to destroy the One Ring and save Middle-earth from the Dark Lord Sauron.",
        },
        {
            "id": 19,
            "title": "Becoming",
            "author": "Michelle Obama",
            "year": 2018,
            "description": "The memoir of the former First Lady of the United States, chronicling her journey from the South Side of Chicago to the White House and beyond.",
        },
        {
            "id": 20,
            "title": "The Catcher in the Rye",
            "author": "J.D. Salinger",
            "year": 1951,
            "description": "A coming-of-age novel about teenage Holden Caulfield's experiences in New York City after being expelled from prep school, exploring themes of alienation and identity.",
        },
        {
            "id": 21,
            "title": "The Subtle Art of Not Giving a F*ck",
            "author": "Mark Manson",
            "year": 2016,
            "description": "A counterintuitive approach to living a good life, arguing that improving your life hinges on becoming comfortable with negative experiences and choosing what to care about.",
        },
        {
            "id": 22,
            "title": "The Hunger Games",
            "author": "Suzanne Collins",
            "year": 2008,
            "description": "A dystopian novel about Katniss Everdeen, who volunteers to take her sister's place in a televised fight to the death in post-apocalyptic North America.",
        },
        {
            "id": 23,
            "title": "The Da Vinci Code",
            "author": "Dan Brown",
            "year": 2003,
            "description": "A mystery thriller following symbologist Robert Langdon as he investigates a murder in the Louvre Museum, uncovering a conspiracy involving the Catholic Church and the Holy Grail.",
        },
        {
            "id": 24,
            "title": "Gone Girl",
            "author": "Gillian Flynn",
            "year": 2012,
            "description": "A psychological thriller about Nick Dunne, who becomes the prime suspect when his wife Amy disappears on their fifth wedding anniversary, revealing dark secrets about their marriage.",
        },
        {
            "id": 25,
            "title": "The Girl with the Dragon Tattoo",
            "author": "Stieg Larsson",
            "year": 2005,
            "description": "A crime thriller about journalist Mikael Blomkvist and hacker Lisbeth Salander as they investigate a wealthy family's dark secrets and a decades-old disappearance.",
        },
        {
            "id": 26,
            "title": "Life of Pi",
            "author": "Yann Martel",
            "year": 2001,
            "description": "A philosophical adventure novel about a young Indian boy who survives 227 days stranded on a lifeboat in the Pacific Ocean with a Bengal tiger named Richard Parker.",
        },
        {
            "id": 27,
            "title": "The Book Thief",
            "author": "Markus Zusak",
            "year": 2005,
            "description": "A novel narrated by Death about a young girl living in Nazi Germany who steals books and shares them with others, including the Jewish man hidden in her basement.",
        },
        {
            "id": 28,
            "title": "Brave New World",
            "author": "Aldous Huxley",
            "year": 1932,
            "description": "A dystopian novel depicting a future society where people are genetically engineered and conditioned for predetermined roles, exploring themes of technology, control, and human nature.",
        },
        {
            "id": 29,
            "title": "The Fault in Our Stars",
            "author": "John Green",
            "year": 2012,
            "description": "A young adult novel about two teenagers with cancer who fall in love after meeting at a support group, exploring themes of life, death, and the meaning of existence.",
        },
        {
            "id": 30,
            "title": "Animal Farm",
            "author": "George Orwell",
            "year": 1945,
            "description": "An allegorical novella about farm animals who rebel against their human farmer, hoping to create a society where animals can be equal, free, and happy.",
        },
        {
            "id": 31,
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "year": 1937,
            "description": "A fantasy adventure about Bilbo Baggins, a hobbit who reluctantly joins a group of dwarves on a quest to reclaim their homeland from the dragon Smaug.",
        },
        {
            "id": 32,
            "title": "Thinking, Fast and Slow",
            "author": "Daniel Kahneman",
            "year": 2011,
            "description": "A groundbreaking exploration of the two systems that drive human thinking: the fast, intuitive system and the slow, deliberative system, and how they shape our decisions.",
        },
        {
            "id": 33,
            "title": "The Outsiders",
            "author": "S.E. Hinton",
            "year": 1967,
            "description": "A coming-of-age novel about Ponyboy Curtis and his struggles with social class conflicts between the working-class 'greasers' and the upper-class 'socs' in 1960s Oklahoma.",
        },
        {
            "id": 34,
            "title": "The Giver",
            "author": "Lois Lowry",
            "year": 1993,
            "description": "A dystopian novel about twelve-year-old Jonas who lives in a seemingly perfect society without pain, suffering, or choice, until he's chosen to learn the truth about his world.",
        },
        {
            "id": 35,
            "title": "One Hundred Years of Solitude",
            "author": "Gabriel García Márquez",
            "year": 1967,
            "description": "A magical realism masterpiece chronicling the multi-generational story of the Buendía family in the fictional town of Macondo, exploring themes of solitude, fate, and Latin American history.",
        },
        {
            "id": 36,
            "title": "The Color Purple",
            "author": "Alice Walker",
            "year": 1982,
            "description": "An epistolary novel about Celie, an African American woman in rural Georgia, exploring themes of racism, sexism, and the power of sisterhood and self-discovery.",
        },
        {
            "id": 37,
            "title": "Norwegian Wood",
            "author": "Haruki Murakami",
            "year": 1987,
            "description": "A coming-of-age novel set in 1960s Tokyo, following Toru Watanabe as he navigates love, loss, and the complexities of relationships during his university years.",
        },
        {
            "id": 38,
            "title": "The Road",
            "author": "Cormac McCarthy",
            "year": 2006,
            "description": "A post-apocalyptic novel about a father and son's journey through a devastated American landscape, exploring themes of survival, love, and hope in the face of despair.",
        },
        {
            "id": 39,
            "title": "Beloved",
            "author": "Toni Morrison",
            "year": 1987,
            "description": "A powerful novel about Sethe, a former slave haunted by the ghost of her daughter, exploring the traumatic legacy of slavery and its impact on individuals and families.",
        },
        {
            "id": 40,
            "title": "The Martian",
            "author": "Andy Weir",
            "year": 2011,
            "description": "A science fiction novel about astronaut Mark Watney, who becomes stranded on Mars and must use his ingenuity and scientific knowledge to survive until rescue is possible.",
        },
        {
            "id": 41,
            "title": "Big Little Lies",
            "author": "Liane Moriarty",
            "year": 2014,
            "description": "A darkly comedic novel about three women whose seemingly perfect lives unravel to the point of murder, exploring themes of domestic violence, friendship, and secrets.",
        },
        {
            "id": 42,
            "title": "The Immortal Life of Henrietta Lacks",
            "author": "Rebecca Skloot",
            "year": 2010,
            "description": "A non-fiction book about the woman whose cancer cells were taken without her knowledge and became one of the most important tools in medical research.",
        },
        {
            "id": 43,
            "title": "Station Eleven",
            "author": "Emily St. John Mandel",
            "year": 2014,
            "description": "A post-apocalyptic novel that follows a group of survivors after a devastating flu pandemic, exploring how art and culture survive in the darkest of times.",
        },
        {
            "id": 44,
            "title": "The Poisonwood Bible",
            "author": "Barbara Kingsolver",
            "year": 1998,
            "description": "A novel about a missionary family's experiences in the Belgian Congo during the 1960s, told through the perspectives of the wife and four daughters.",
        },
        {
            "id": 45,
            "title": "A Thousand Splendid Suns",
            "author": "Khaled Hosseini",
            "year": 2007,
            "description": "A powerful novel about the friendship between two Afghan women from different generations, set against the backdrop of Afghanistan's tumultuous recent history.",
        },
        {
            "id": 46,
            "title": "The Help",
            "author": "Kathryn Stockett",
            "year": 2009,
            "description": "A novel set in 1960s Mississippi, focusing on the relationship between African American maids and their white employers, exploring themes of racism and social change.",
        },
        {
            "id": 47,
            "title": "Ready Player One",
            "author": "Ernest Cline",
            "year": 2011,
            "description": "A science fiction novel set in a dystopian 2045, where people escape reality through a virtual world called the OASIS, following Wade Watts' quest to find a hidden treasure.",
        },
        {
            "id": 48,
            "title": "The Girl on the Train",
            "author": "Paula Hawkins",
            "year": 2015,
            "description": "A psychological thriller about Rachel, an alcoholic who becomes entangled in a missing person investigation after witnessing something shocking from her daily train commute.",
        },
        {
            "id": 49,
            "title": "Wild",
            "author": "Cheryl Strayed",
            "year": 2012,
            "description": "A memoir about the author's solo hike along the Pacific Crest Trail as a way to recover from personal tragedies, exploring themes of grief, healing, and self-discovery.",
        },
        {
            "id": 50,
            "title": "The Sixth Extinction",
            "author": "Elizabeth Kolbert",
            "year": 2014,
            "description": "A non-fiction book examining the ongoing sixth mass extinction of species caused by human activity, combining scientific research with field reporting from around the world.",
        },
    ]

    return books


def save_books_to_json(books, filepath):
    """
    Save the list of books to a JSON file.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)

    logger.info(f"Books saved to {filepath}")
    return filepath


def main():
    """Main function to generate and save book data."""
    logger.info("Starting book data generation...")
    books = generate_book_descriptions()

    # Define the output directory
    output_path = "data/book_descriptions.json"

    # Save to JSON File
    save_books_to_json(books, output_path)

    logger.info("Book data generation completed.")
    logger.info(f"Total books generated: {len(books)}")


if __name__ == "__main__":
    main()
