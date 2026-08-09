import Foundation
import PDFKit

guard CommandLine.arguments.count >= 2 else {
    fputs("usage: extract_pdf.swift <pdf>\n", stderr)
    exit(2)
}

let path = CommandLine.arguments[1]
guard let document = PDFDocument(url: URL(fileURLWithPath: path)) else {
    fputs("could not open \(path)\n", stderr)
    exit(1)
}

print("PAGES\t\(document.pageCount)")
for index in 0..<document.pageCount {
    let text = document.page(at: index)?.string ?? ""
    print("\n<<<PAGE \(index + 1)>>>\n\(text)")
}
