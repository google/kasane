class Kasane < Formula
  include Language::Python::Virtualenv

  desc "Kasane is a layering tool for kubernetes"
  homepage "https://github.com/google/kasane"
  url "https://github.com/google/kasane/archive/0.1.3.tar.gz"
  sha256 "a859e566b588fe74818d4c2270ba66263046f44fed7e9ecd5af582f0955b92e2"
  head "https://github.com/google/kasane.git"

  depends_on "python"

  resource "click" do
    url "https://files.pythonhosted.org/packages/95/d9/c3336b6b5711c3ab9d1d3a80f1a3e2afeb9d8c02a7166462f6cc96570897/click-6.7.tar.gz"
    sha256 "f15516df478d5a56180fbf80e68f206010e6d160fc39fa508b65e035fd75130b"
  end

  resource "Jinja2" do
    url "https://files.pythonhosted.org/packages/56/e6/332789f295cf22308386cf5bbd1f4e00ed11484299c5d7383378cf48ba47/Jinja2-2.10.tar.gz"
    sha256 "f84be1bb0040caca4cea721fcbbbbd61f9be9464ca236387158b0feea01914a4"
  end

  resource "MarkupSafe" do
    url "https://files.pythonhosted.org/packages/4d/de/32d741db316d8fdb7680822dd37001ef7a448255de9699ab4bfcbdf4172b/MarkupSafe-1.0.tar.gz"
    sha256 "a6be69091dac236ea9c6bc7d012beab42010fa914c459791d627dad4910eb665"
  end

  resource "jsonnet" do
    url "https://files.pythonhosted.org/packages/4a/f5/a0a41ac1f141a62c966291feff15e1829147462e95041bdc5fee1dcd7e0f/jsonnet-0.11.2.tar.gz"
    sha256 "3201ca48b0ddc4d65a534686436cd435491addcf26346b07dbd69b38f66f4f8f"
  end

  resource "requests" do
    url "https://files.pythonhosted.org/packages/54/1f/782a5734931ddf2e1494e4cd615a51ff98e1879cbe9eecbdfeaf09aa75e9/requests-2.19.1.tar.gz"
    sha256 "ec22d826a36ed72a7358ff3fe56cbd4ba69dd7a6718ffd450ff0e9df7a47ce6a"
  end

  resource "certifi" do
    url "https://files.pythonhosted.org/packages/4d/9c/46e950a6f4d6b4be571ddcae21e7bc846fcbb88f1de3eff0f6dd0a6be55d/certifi-2018.4.16.tar.gz"
    sha256 "13e698f54293db9f89122b0581843a782ad0934a4fe0172d2a980ba77fc61bb7"
  end

  resource "chardet" do
    url "https://files.pythonhosted.org/packages/fc/bb/a5768c230f9ddb03acc9ef3f0d4a3cf93462473795d18e9535498c8f929d/chardet-3.0.4.tar.gz"
    sha256 "84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae"
  end

  resource "idna" do
    url "https://files.pythonhosted.org/packages/65/c4/80f97e9c9628f3cac9b98bfca0402ede54e0563b56482e3e6e45c43c4935/idna-2.7.tar.gz"
    sha256 "684a38a6f903c1d71d6d5fac066b58d7768af4de2b832e426ec79c30daa94a16"
  end

  resource "urllib3" do
    url "https://files.pythonhosted.org/packages/3c/d2/dc5471622bd200db1cd9319e02e71bc655e9ea27b8e0ce65fc69de0dac15/urllib3-1.23.tar.gz"
    sha256 "a68ac5e15e76e7e5dd2b8f94007233e01effe3e50e8daddf69acfd81cb686baf"
  end

  resource "ruamel.yaml" do
    url "https://files.pythonhosted.org/packages/63/a5/dba37230d6cf51f4cc19a486faf0f06871d9e87d25df0171b3225d20fc68/ruamel.yaml-0.15.45.tar.gz"
    sha256 "096691b0958514da21d19ae40255569f027b5b90530c55faf1d74ff16b2f256b"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    # TODO: version check
    # assert_match version.to_s, shell_output("#{bin}/kasane --version")

    mkdir testpath do
      open("Kasanefile", "w") do |f|
        f.write <<~YAML
          layers:
            - test.yaml
        YAML
      end

      open("test.yaml", "w") do |f|
        f.write <<~YAML
          ---
          kind: Dummy
          metadata:
            name: dummy
        YAML
      end

      system "#{bin}/kasane", "show"
    end
  end
end
