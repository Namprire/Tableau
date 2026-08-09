import AppKit
import Foundation
import PDFKit

guard CommandLine.arguments.count >= 4 else {
    fputs("usage: render_pages.swift <pdf> <output-dir> <page1,page2,...>\n", stderr)
    exit(2)
}

let pdfPath = CommandLine.arguments[1]
let outputDir = CommandLine.arguments[2]
let requestedPages = CommandLine.arguments[3]
    .split(separator: ",")
    .compactMap { Int($0) }

guard let document = PDFDocument(url: URL(fileURLWithPath: pdfPath)) else {
    fputs("could not open \(pdfPath)\n", stderr)
    exit(1)
}

try FileManager.default.createDirectory(
    at: URL(fileURLWithPath: outputDir),
    withIntermediateDirectories: true
)

for pageNumber in requestedPages {
    let pageIndex = pageNumber - 1
    guard pageIndex >= 0, pageIndex < document.pageCount,
          let page = document.page(at: pageIndex) else { continue }
    let bounds = page.bounds(for: .mediaBox)
    let targetWidth: CGFloat = 1600
    let targetSize = NSSize(width: targetWidth, height: targetWidth * bounds.height / bounds.width)
    let image = page.thumbnail(of: targetSize, for: .mediaBox)
    guard let tiff = image.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: tiff),
          let png = bitmap.representation(using: .png, properties: [:]) else { continue }
    let name = String(format: "page-%03d.png", pageNumber)
    let outputURL = URL(fileURLWithPath: outputDir).appendingPathComponent(name)
    try png.write(to: outputURL)
    print(outputURL.path)
}
