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
install-requirements:
	@echo "🚀 Installing from requirements.txt..."
	@uv pip install -r requirements.txt
	@echo "✅ Packages installed successfully!"

export-requirements:
	@echo "🚀 Generating requirements.txt..."
	@uv pip freeze > requirements.txt
	@echo "✅ requirements.txt has been created successfully!"

# 🧹 Cleanup
clean:
	@echo "🧹 Cleaning up temporary files..."
	del /s /q __pycache__\*
	del /s /q *.pyc
	del /s /q *.pyo
	rmdir /s /q .pytest_cache
	@echo "✅ Cleanup complete!"
