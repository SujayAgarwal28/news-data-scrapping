@echo off
REM ============================================================================
REM INTERACTIVE NEWS SCRAPER LAUNCHER
REM ============================================================================
REM Simple menu-driven interface for news scraping
REM No complex command-line arguments needed!
REM
REM Author: StockBus Team
REM Created: October 9, 2025
REM ============================================================================

echo.
echo ========================================================================
echo    STOCKBUS TRADE PULSE - INTERACTIVE NEWS SCRAPER
echo ========================================================================
echo.
echo Starting menu-driven scraper...
echo.

cd /d "%~dp0"
python interactive_scraper.py

pause
