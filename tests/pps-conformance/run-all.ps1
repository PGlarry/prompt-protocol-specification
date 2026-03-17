$ErrorActionPreference = 'Stop'

Write-Host "Hashing all examples..."
npm run pps:hash:all | Out-Host

Write-Host "Validating all examples..."
npm run pps:validate:all | Out-Host

Write-Host "Policy checks..."
npm run pps:policy | Out-Host

Write-Host "Adversarial auto-fix -> rehash -> revalidate"
npm run pps:fix:adv | Out-Host
npm run pps:rehash:adv | Out-Host
npm run pps:validate:adv | Out-Host
npm run pps:policy:adv | Out-Host

Write-Host "RAG citations auto-fix -> rehash -> revalidate"
node tests/pps-conformance/auto_fix.js spec/examples/rag_citations_required.json --write | Out-Host
npm run pps:hash:rag | Out-Host
npm run pps:validate:rag | Out-Host
npm run pps:policy:rag | Out-Host

Write-Host "GDPR auto-fix hint (no_pii) -> rehash -> revalidate"
node tests/pps-conformance/auto_fix.js spec/examples/gdpr_missing_no_pii.json --write | Out-Host
npm run pps:hash:gdpr | Out-Host
npm run pps:validate:gdpr | Out-Host
npm run pps:policy:gdpr | Out-Host

Write-Host "Done."


