# PostgreSQL Password Reset Helper
Write-Host "PostgreSQL Password Reset Instructions" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "OPTION 1 - Use pgAdmin (EASIEST):" -ForegroundColor Green
Write-Host "1. Open pgAdmin 4"
Write-Host "2. Right-click on PostgreSQL 18 server"
Write-Host "3. Select 'Properties'"
Write-Host "4. Enter the current password you know"
Write-Host "5. Go to 'Definition' tab"
Write-Host "6. Change password to: passperi"
Write-Host "7. Click Save"
Write-Host ""
Write-Host "OPTION 2 - Temporarily allow trust authentication:" -ForegroundColor Yellow
Write-Host "CAUTION: This temporarily disables password protection!"
Write-Host ""
Write-Host "Run these commands AS ADMINISTRATOR:" -ForegroundColor Red
Write-Host '1. Stop-Service postgresql-x64-18'
Write-Host '2. Backup: Copy-Item "C:\Program Files\PostgreSQL\18\data\pg_hba.conf" "C:\Program Files\PostgreSQL\18\data\pg_hba.conf.backup"'
Write-Host '3. Edit C:\Program Files\PostgreSQL\18\data\pg_hba.conf'
Write-Host '   Change all "scram-sha-256" to "trust"'
Write-Host '4. Start-Service postgresql-x64-18'
Write-Host '5. Run: psql -U postgres -d postgres -c "ALTER USER postgres WITH PASSWORD ''passperi'';"'
Write-Host '6. Restore: Copy-Item "C:\Program Files\PostgreSQL\18\data\pg_hba.conf.backup" "C:\Program Files\PostgreSQL\18\data\pg_hba.conf" -Force'
Write-Host '7. Restart-Service postgresql-x64-18'
Write-Host ""
Write-Host "OPTION 3 - Just tell me the CORRECT password:" -ForegroundColor Magenta
Write-Host "If you know the current postgres password, just update the .env file with it!"
Write-Host ""
