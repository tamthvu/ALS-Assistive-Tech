class TrieNode {
  constructor() {
    this.children = new Map();
    this.wordCount = 0;
    this.isEndOfWord = false;
  }
}

class Trie {
  constructor() {
    this.root = new TrieNode();
  }

  insert(word, count) {
    let node = this.root;
    for (const char of word) {
      if (!node.children.has(char)) {
        node.children.set(char, new TrieNode());
      }
      node = node.children.get(char);
    }
    node.isEndOfWord = true;
    node.wordCount = count;
  }

  search(prefix) {
    let node = this.root;
    for (const char of prefix) {
      if (!node.children.has(char)) {
        return [];
      }
      node = node.children.get(char);
    }
    return this.getPredictiveText(node, prefix);
  }

  getPredictiveText(node, prefix) {
    const suggestions = [];
    const queue = [[node, prefix]];

    while (queue.length > 0) {
      const [currentNode, currentPrefix] = queue.shift();

      if (currentNode.isEndOfWord) {
        suggestions.push({ word: currentPrefix, count: currentNode.wordCount });
      }

      for (const [char, child] of currentNode.children) {
        queue.push([child, currentPrefix + char]);
      }
    }

    return suggestions.sort((a, b) => b.count - a.count);
  }
}

const fs = require("fs");
const trie = new Trie();

// Read the words.txt file and insert words into the Trie
const wordsFile = fs.readFileSync("words.txt", "utf-8");
const lines = wordsFile.split("\n");
for (const line of lines) {
  const [word, count] = line.split(" ");
  trie.insert(word, parseInt(count));
}

// Get predictive text based on user input
const readline = require("readline");
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.on("line", (input) => {
  const suggestions = trie.search(input);
  console.log(`Suggestions for "${input}":`);
  for (const { word, count } of suggestions.slice(0, 3)) {
    // Take the top 3 in list
    console.log(`${word} (${count})`);
  }
  console.log();d
});
