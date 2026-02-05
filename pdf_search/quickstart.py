"""Quick start demo for PDF semantic search."""
from pathlib import Path
from search_engine import SemanticSearchEngine
from rich.console import Console

console = Console()


def main():
    """Run a quick demo of the search engine."""
    
    console.print("\n[bold cyan]PDF Semantic Search Engine - Quick Start[/bold cyan]\n")
    
    # Initialize engine
    console.print("1. Initializing search engine...")
    engine = SemanticSearchEngine()
    
    if not engine.initialize():
        console.print("[red]Failed to initialize. Make sure Endee is running![/red]")
        console.print("\nStart Endee with: docker-compose up")
        return
    
    console.print("[green]✓ Engine initialized[/green]\n")
    
    # Check for PDFs
    pdf_dir = Path("pdfs")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        console.print(f"[yellow]No PDF files found in {pdf_dir}/[/yellow]")
        console.print("\nPlease add some PDF files to the 'pdfs' directory and run again.\n")
        return
    
    console.print(f"Found {len(pdf_files)} PDF file(s):")
    for pdf in pdf_files:
        console.print(f"  • {pdf.name}")
    console.print()
    
    # Ingest PDFs
    console.print("2. Ingesting PDFs...")
    if not engine.ingest_pdfs():
        console.print("[red]Failed to ingest PDFs[/red]")
        return
    
    console.print("\n[green]✓ PDFs ingested successfully[/green]\n")
    
    # Example searches
    console.print("3. Running example searches...\n")
    
    example_queries = [
        "What is machine learning?",
        "How does neural network work?",
        "Explain data preprocessing"
    ]
    
    for query in example_queries:
        console.print(f"[bold cyan]Query:[/bold cyan] {query}")
        results = engine.search(query, top_k=2)
        
        if results:
            for i, result in enumerate(results, 1):
                metadata = result.get('metadata', {})
                score = result.get('score', 0.0)
                text = metadata.get('text', '')[:150]
                
                console.print(f"  {i}. [Score: {score:.4f}] {metadata.get('file_name')} (p.{metadata.get('page')})")
                console.print(f"     {text}...\n")
        else:
            console.print("  [yellow]No results found[/yellow]\n")
    
    console.print("[bold green]Demo complete! Use 'python cli.py interactive' for interactive search.[/bold green]\n")


if __name__ == "__main__":
    main()
