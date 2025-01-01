# 🛠️ Project Makefile

.PHONY: help install-requirements export-requirements clean

# 🎯 Default target
help:
	@echo "📖 Usage:"
	@echo "       make help           			- Show this help message"
	@echo "📦 Dependencies:"
	@echo "       make install-requirements   	- Install requirements.txt"
	@echo "       make export-requirements   	- Generate requirements.txt"
	@echo "🧹 Cleanup:"
	@echo "       make clean          			- Clean up temporary files"

# 📦 Dependencies
export-requirements:
	@echo "🚀 Generating requirements.txt..."
	@pip freeze > requirements.txt
	@echo "✅ requirements.txt has been created successfully!"

install-requirements:
	@echo "🚀 Installing from requirements.txt..."
	@pip install -r requirements.txt
	@echo "✅ Packages installed successfully!"

# 🧹 Cleanup
clean:
	@echo "🧹 Cleaning up temporary files..."
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name '*.pyc' -exec rm -rf {} +
	@find . -name '*.pyo' -exec rm -rf {} +
	@find . -name '*.pytest_cache' -exec rm -rf {} +
	@echo "✅ Cleanup complete!"

